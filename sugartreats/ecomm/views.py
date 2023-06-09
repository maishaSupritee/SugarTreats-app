from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,"ecomm/dashboard.html")

def products(request):
    return render(request,"ecomm/products.html")

def customers(request):
    return render(request,"ecomm/customers.html")