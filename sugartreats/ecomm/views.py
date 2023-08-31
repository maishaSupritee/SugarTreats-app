from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.forms import (
    inlineformset_factory,
)  # we need this import to use inline formsets
from django.db import transaction
from .models import *
from .forms import *


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
    order_details = []  # a list
    total_rewards = 0
    for order in orders:
        order_rewards = 0
        order_items = OrderItem.objects.filter(orders=order)
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
    }
    return render(request, "ecomm/profile.html", context)

def createOrder(request, pk):
    customer = Customer.objects.get(id=pk)

    if request.method == "POST":
        # transaction. atomic is a context manager to ensure that the Order and OrderItem instances 
        # are created within the same database transaction.
        with transaction.atomic():
            order = Order.objects.create(customer=customer, status="Pending")
            OrderItemFormset = inlineformset_factory(
                Order, OrderItem, fields=["product", "quantity"]
            )
            formset = OrderItemFormset(request.POST, instance=order)

            if formset.is_valid():
                print("Formset is valid")
                for form in formset:
                    product = form.cleaned_data.get("product")
                    quantity = form.cleaned_data.get("quantity")
                    print("Product:", product, "Quantity:", quantity)

                    if product and quantity > 0:
                        order_item = OrderItem.objects.create(
                            order=order, product=product, quantity=quantity
                        )
                        order.order_items.add(order_item)
                return redirect("profile", pk=customer.id)
            else:
                print("Formset errors:", formset.errors)
    else:
        OrderItemFormset = inlineformset_factory(
            Order, OrderItem, fields=["product", "quantity"]
        )
        formset = OrderItemFormset(instance=Order())

    context = {"formset": formset}
    return render(request, "ecomm/order_form.html", context)


def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(
        instance=order
    )  # the item instance we are going to fill out in our form, this fills out all the fields in the form with the order's details
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("/")
    context = {"form": form}
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
