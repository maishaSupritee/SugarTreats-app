from django.forms import ModelMultipleChoiceField, ModelForm, CheckboxSelectMultiple
from .models import * #we can use .models because they are in the same folder

class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = "__all__"