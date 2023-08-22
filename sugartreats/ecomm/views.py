from django.http import HttpResponse
from django.shortcuts import render
from .models import*

# Create your views here.
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    products = Product.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status = "Delivered").count()
    fulfilled = orders.filter(status = "Fulfilled").count()
    pending = orders.filter(status = "Pending").count()
    context = {
        "orders": orders, 
        "customers": customers, 
        "products": products,
        "total_customers": total_customers,
        "total_orders": total_orders,
        "delivered": delivered,
        "pending": pending,
        "fulfilled": fulfilled
        }
    return render(request,"ecomm/dashboard.html", context)

def products(request):
    products = Product.objects.all()
    return render(request,"ecomm/products.html", {"products": products})

def customers(request):
    customer = Customer.objects.all()
    context = {"customer":customer}
    return render(request,"ecomm/customers.html", context)

def profiles(request,pk):
    customer = Customer.objects.get(id=pk) #querying the customer by their id, and the id will be the primary key we are putting in the url path
    context = {"customer": customer}
    return render(request, "ecomm/profile.html", context)

def createOrder(request):
    context = {}
    return render(request, "ecomm/order_form.html", context)