from django.forms import ModelForm
from .models import *


class OrderForm(ModelForm):
    class Meta:
        # need a minimum of two fields for a form
        model = Order  # which model from models.py I'm making the form for
        fields = "__all__"  # we are allowing all fields of the model in our form
        # if we wanted specific fields of the model to only be included, needed a list like fields = ["customer","products"]
