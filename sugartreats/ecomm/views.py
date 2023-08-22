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
    return render(request,"ecomm/customers.html")