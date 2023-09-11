from django.forms import ModelMultipleChoiceField, ModelForm, CheckboxSelectMultiple
from django import forms
from .models import * #we can use .models because they are in the same folder

class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = "__all__"

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ["note", "status"]
    