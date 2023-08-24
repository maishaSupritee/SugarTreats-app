from django.forms import ModelForm
from .models import * #we can use .models because they are in the same folder

class OrderForm(ModelForm): #NameofmodelForm used as name of class
    class Meta:
        #need a minimum of 2 fields for a form
        model = Order #which model i'm making a form for
        fields = "__all__" #we are allowing all fields of the model in our form
        #if we wanted specific fields, we would have made a list like fields = ["customer", "product"]