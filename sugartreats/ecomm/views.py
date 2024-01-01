from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.forms import (
    inlineformset_factory, modelform_factory, BaseInlineFormSet
)  # we need this import to use inline formsets
from django.db import transaction
from .models import *
from .forms import *
from .filters import *
from django.db.models import Q

from django.http import JsonResponse
from .serializers import *

#Views for REST API
def customer_list(request):
    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    return JsonResponse({"customers": serializer.data}, safe=False)

def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return JsonResponse({"products": serializer.data}, safe=False)

def order_list(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return JsonResponse({"orders": serializer.data}, safe=False)

def orderItem_list(request):
    orderItems = OrderItem.objects.all()
    serializer = OrderItemSerializer(orderItems, many=True)
    return JsonResponse({"orderItems": serializer.data}, safe=False)

# Create your views here.
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    products = Product.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    fulfilled = orders.filter(status="Fulfilled").count()
    pending = orders.filter(status="Pending").count()
    list = orders.order_by("-date_created")
    ordered_list = list[:5]  # returns first five objects
    context = {
        "orders": orders,
        "customers": customers,
        "products": products,
        "total_customers": total_customers,
        "total_orders": total_orders,
        "delivered": delivered,
        "pending": pending,
        "fulfilled": fulfilled,
        "ordered_list": ordered_list,
    }
    return render(request, "ecomm/dashboard.html", context)


def products(request):
    products = Product.objects.all().order_by("name")
    return render(request, "ecomm/products.html", {"products": products})


def customers(request):
    customers = Customer.objects.all().order_by("name")
    context = {"customers": customers}
    return render(request, "ecomm/customers.html", context)


def orders(request):
    orders = Order.objects.all().order_by(
        "-date_created", "customer"
    )  # the minus means we are ordering by reverse of date_created, so last order first
    context = {"orders": orders}
    return render(request, "ecomm/orders.html", context)


def profiles(request, pk):
    customer = Customer.objects.get(
        id=pk
    )  # querying the customer by their id, and the id will be the primary key we are putting in the url path
    orders = Order.objects.filter(customer=customer)
    orderItems = OrderItem.objects.filter(order__customer = customer)

    #Work for the search filter
    orderfilter = OrderFilter(request.GET, queryset = orders) #filter the queryset data down based on what the request.GET data is
    itemfilter = ItemFilter(request.GET, queryset = orderItems)
    
     # Apply filters for Order attributes
    if orderfilter.qs:
        orders = orderfilter.qs

    # Apply filters for OrderItem attributes
    if itemfilter.qs:
        orderItems = itemfilter.qs

    # Combine the results based on the filter criteria
    orders = orders.filter(id__in=orderItems.values_list('order_id', flat=True))
    #values_list returns a queryset as a list of tuples for ex. QuerySet [(1,2),(2,3)]
    #since we are using values_list with a single field order_id, 
    #we use flat=True and get QuerySet [1, 2] instead of QuerySet [ (1,), (2,)]
    

    #work for getting rewards information
    order_details = []  # a list
    total_rewards = 0
    for order in orders:
        order_rewards = 0
        order_items = OrderItem.objects.filter(order=order)
        for order_item in order_items:
            order_rewards += order_item.product.rewards * order_item.quantity
        total_rewards += order_rewards
        order_details.append(
            {"order": order, "order_items": order_items, "order_rewards": order_rewards}
        )
    context = {
        "customer": customer,
        "orders": orders,
        "order_details": order_details,
        "total_rewards": total_rewards,
        "orderfilter": orderfilter,
        "itemfilter" : itemfilter,
    }
    return render(request, "ecomm/profile.html", context)

def createOrder(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == "POST":
        order_form = OrderForm(request.POST) #just for handling note and status
        # transaction.atomic is a context manager to ensure that the Order and OrderItem instances
        # are created within the same database transaction.
        with transaction.atomic():
            order = Order.objects.create(customer=customer)
            OrderItemFormset = inlineformset_factory(
                Order, OrderItem, fields=('product', 'quantity'), extra=5
            )
            formset = OrderItemFormset(request.POST, instance=order, queryset=OrderItem.objects.none())

            if formset.is_valid() and order_form.is_valid():
                note = order_form.cleaned_data.get("note")
                status = order_form.cleaned_data.get("status")

                order.note = note
                order.status = status
                order.save()
                for form in formset:
                    product = form.cleaned_data.get("product")
                    quantity = form.cleaned_data.get("quantity")

                    if product and quantity > 0:
                        order_item = OrderItem.objects.create(
                            order=order, product=product, quantity=quantity
                        )
                        order.order_items.add(order_item)
                return redirect("profile", pk=customer.id)
            else:
                print("Formset errors:", formset.errors)
    else:
        order_form = OrderForm()
        OrderItemFormset = inlineformset_factory(
            Order, OrderItem, fields=('product', 'quantity'), extra=5
        )
        formset = OrderItemFormset(instance=Order())
    context = {"formset": formset, "order_form": order_form}
    return render(request, "ecomm/order_form.html", context)

def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    customer = Customer.objects.get(orders=order)
    order_items = order.order_items.all()

    OrderItemFormset = inlineformset_factory(
        Order, OrderItem, fields=('product', 'quantity'), extra=5
    )

    if request.method == "POST":
        order_form = OrderForm(request.POST, instance=order)
        formset = OrderItemFormset(request.POST, instance=order)
        if formset.is_valid() and order_form.is_valid():
            note = order_form.cleaned_data.get("note")
            status = order_form.cleaned_data.get("status")

            order.note = note
            order.status = status
            order.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.order = order
                instance.save()
                order.order_items.add(instance)
            formset.save()
            return redirect("profile", pk=customer.id)
        else:
            print("Formset errors:", formset.errors)
    else:
        order_form = OrderForm(instance=order)
        formset = OrderItemFormset(instance=order)
    context = {"formset": formset, "order_form": order_form}
    return render(request, "ecomm/order_form.html", context)



def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    order_items = OrderItem.objects.filter(orders=order)
    if request.method == "POST":
        order_items.delete()  # deleting all the order items associated with an order
        order.delete()
        return redirect("/")  # just / returns us to home page
    context = {"order": order}
    return render(request, "ecomm/delete.html", context)
