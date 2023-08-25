from django.urls import path
from .import views

urlpatterns = [
    path("", views.home, name = "home"),
    path("products/", views.products, name = "products"),
    path("customers/", views.customers, name = "customers"),
    path("profile/<str:pk>/", views.profiles, name = "profile"), #adding a string variable here by the name of pk, this pk and the one we use in the customers function must have the same name to work
    path("create_order/<str:pk>/", views.createOrder, name = "create_order"),
    path("update_order/<str:pk>/", views.updateOrder, name = "update_order"),
    path("delte_order/<str:pk>/", views.deleteOrder, name = "delete_order")
    ]
