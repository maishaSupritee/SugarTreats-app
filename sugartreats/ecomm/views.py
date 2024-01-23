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

#for REST API work
from django.http import JsonResponse
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

#for user login/registration
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages #to use flash messages

#Views for REST API
@api_view(['GET','POST'])
def customer_list(request, format=None):
    if request.method == 'GET':
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CustomerSerializer(data=request.data) #serialize the data sent with POST
        if serializer.is_valid(): #if data is valid
            serializer.save() #save a new customer with that data
            return Response(serializer.data, status=status.HTTP_201_CREATED) #return the customer data as well as status code

@api_view(['GET', 'PUT', 'DELETE'])
def customer_detail(request, pk, format=None):
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist: #if customer doesn't exist display error 404
        return Response(status = status.HTTP_404_NOT_FOUND) 
    if request.method == 'GET':
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
    elif request.method == 'PUT': #update individual customer info
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save() #save customer with the updated info
            return Response(serializer.data) #return the updated customer
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE': #delete any individual customer
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def product_list(request, format=None):
    if request.method == 'GET':    
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk, format=None):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist: #if product doesn't exist display error 404
        return Response(status = status.HTTP_404_NOT_FOUND) 
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT': #update individual product info
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save() #save product with the updated info
            return Response(serializer.data) #return the updated product
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE': #delete any individual product
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET','POST'])
def order_list(request, format=None):
    if request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            # Create order items
            order_items_data = request.data.get('order_items', [])
            for order_item_data in order_items_data:
                # Convert dictionary to OrderItem instance
                order_item_serializer = OrderItemSerializer(data=order_item_data)
                if order_item_serializer.is_valid():
                    order_item_serializer.save(order=order)  # Pass the order instance to set the relationship
                else:
                    # Return a response in case of invalid order item
                    return Response(order_item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def order_detail(request, pk, format=None):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist: #if order doesn't exist display error 404
        return Response(status = status.HTTP_404_NOT_FOUND) 
    if request.method == 'GET':
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    elif request.method == 'PUT': #update individual order info
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save() #save order with the updated info
            return Response(serializer.data) #return the updated order
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE': #delete any individual order
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET']) #order_items should only be automatically created when a new order is created
def orderItem_list(request, format=None):
    if request.method=='GET':
        orderItems = OrderItem.objects.all()
        serializer = OrderItemSerializer(orderItems, many=True)
        return Response(serializer.data)
    
@api_view(['GET', 'PUT', 'DELETE'])
def order_item_detail(request, pk, format=None):
    try:
        order_item = OrderItem.objects.get(pk=pk)
    except OrderItem.DoesNotExist: #if order_item doesn't exist display error 404
        return Response(status = status.HTTP_404_NOT_FOUND) 
    if request.method == 'GET':
        serializer = OrderItemSerializer(order_item)
        return Response(serializer.data)
    elif request.method == 'PUT': #update individual order_item info
        serializer = OrderItemSerializer(order_item, data=request.data)
        if serializer.is_valid():
            serializer.save() #save order_item with the updated info
            return Response(serializer.data) #return the updated order_item
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE': #delete any individual order_item
        order_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Create your views here.
def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST) 
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username') #just get the username from the form
            messages.success(request, "Account successfully created for " + user) #flash message that will display after a user has registered
            return redirect('login') #redirect user to login page once they are registered

    context = {'form': form}
    return render(request, "ecomm/register.html", context)

def login(request):
    return render(request, "ecomm/login.html")

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
