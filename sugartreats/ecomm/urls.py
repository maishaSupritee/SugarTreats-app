from django.urls import path
from .import views

urlpatterns = [
    path("", views.home, name = "home"),
    path("register/", views.register, name = "register"),
    path("login/", views.login, name = "login"),
    path("products/", views.products, name = "products"),
    path("customers/", views.customers, name = "customers"),
    path("orders/", views.orders, name = "orders"),
    path("profile/<str:pk>/", views.profiles, name = "profile"), #adding a string variable here by the name of pk, this pk and the one we use in the customers function must have the same name to work
    path("create_order/<str:pk>/", views.createOrder, name = "create_order"),
    path("update_order/<str:pk>/", views.updateOrder, name = "update_order"),
    path("delete_order/<str:pk>/", views.deleteOrder, name = "delete_order"),
    ]
