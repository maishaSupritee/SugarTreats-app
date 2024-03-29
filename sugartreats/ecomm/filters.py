import django_filters
from .models import *
from django_filters import DateFilter, CharFilter

class OrderFilter(django_filters.FilterSet):
    startdate=DateFilter(field_name="date_created", lookup_expr='gte') #gte means greater than or equal to, lte means less than or equal to
    enddate=DateFilter(field_name="date_created", lookup_expr='lte') #lookup is allowing us to manually write down the datees 
    note = CharFilter(field_name="note", lookup_expr='icontains') #icontains means ignore lower/upper case, works for any
    class Meta: #need a minimum of 2 attributes
        model = Order
        fields = "__all__"
        exclude = ['customer', 'date_created', 'order_items']
    
class ItemFilter(django_filters.FilterSet):
    class Meta:
        model = OrderItem
        fields = "__all__"
        