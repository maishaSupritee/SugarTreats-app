from django.forms import ModelMultipleChoiceField, ModelForm, CheckboxSelectMultiple
from django import forms
from .models import * #we can use .models because they are in the same folder

#For user creation and login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm): #replica of django's default form
    class Meta:
        model = User
        #get the field names of the default django form from the official documentation of UserCreationForm
        fields = ["username", "email", "password1", "password2"]

class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = "__all__"

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ["note", "status"]
   