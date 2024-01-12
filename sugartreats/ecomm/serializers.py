from rest_framework import serializers
from .models import *

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone', 'date_created']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'product_num', 'description', 'category', 'price', 'tags', 'rewards']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'order']

class OrderSerializer(serializers.ModelSerializer):
    #Custom field, will call the get_order_items method to determine the value of this field
    order_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'customer', 'order_items', 'note', 'status', 'date_created']

    #get_order_items retrieves the value of the order_items field, obj is the instance of the Order being created
    def get_order_items(self, obj):
        order_items = OrderItem.objects.filter(order=obj) #filters the OrderItem instances based on the order field
        serializer = OrderItemSerializer(order_items, many=True)
        return serializer.data
    
    #have to use custom create() method as we need to create order_items whenever we create a new order
    #creates a new Order instance and then iterates through the order_items_data to create associated OrderItem instances.
    def create(self, validated_data):
        #validated_data is a dictionary of input data sent during request
        order_items_data = validated_data.pop('order_items', []) #get the value associated with key "order_items", default is empty list []
        order = Order.objects.create(**validated_data)

        for order_item_data in order_items_data:
            OrderItem.objects.create(order=order, **order_item_data)

        return order

