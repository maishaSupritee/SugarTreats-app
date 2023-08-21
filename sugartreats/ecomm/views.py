from django.http import HttpResponse
from django.shortcuts import render
from .models import*

# Create your views here.
def home(request):
    return render(request,"ecomm/dashboard.html")

def products(request):
    products = Product.objects.all()
    return render(request,"ecomm/products.html", {"products": products})

def customers(request):
    return render(request,"ecomm/customers.html")