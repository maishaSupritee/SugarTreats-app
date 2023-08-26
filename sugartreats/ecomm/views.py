from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.forms import (
    inlineformset_factory,
)  # we need this import to use inline formsets
from django.db.models import Count
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
    products = Product.objects.all()
    return render(request, "ecomm/products.html", {"products": products})


def customers(request):
    customers = Customer.objects.all()
    context = {"customers": customers}
    return render(request, "ecomm/customers.html", context)


def orders(request):
    orders = Order.objects.all()
    context = {"orders": orders}
    return render(request, "ecomm/orders.html", context)


def profiles(request, pk):
    customer = Customer.objects.get(
        id=pk
    )  # querying the customer by their id, and the id will be the primary key we are putting in the url path
    context = {"customer": customer}
    return render(request, "ecomm/profile.html", context)


def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=("order_items", "note", "status")
    )
    customer = Customer.objects.get(id=pk)
    form = OrderForm(
        initial={"customer": customer}
    )  # the instance of the customer attribute will be the customer we queried with the id
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("profile", pk=customer.id)
    context = {"form": form}
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
    if request.method == "POST":
        order.delete()
        return redirect("/")  # just / returns us to home page
    context = {"order": order}
    return render(request, "ecomm/delete.html", context)
