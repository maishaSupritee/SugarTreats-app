from django.forms import ModelMultipleChoiceField, ModelForm, CheckboxSelectMultiple
from django import forms
from .models import * #we can use .models because they are in the same folder

class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = "__all__"

class OrderForm(forms.Form):
    note = forms.CharField(max_length=300, required = False)
    status = forms.ChoiceField(choices=Order.STATUS, required=True)