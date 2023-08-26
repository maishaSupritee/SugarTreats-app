from django.db import models


# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        result = "(C" + str(self.id) + ") " + str(self.name) #adding str infront of self.name because name could be null which could give error
        return result

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True,)

    def __str__(self):
        return str(self.name) #adding str infront of self.name because name could be null which could give error

class Product(models.Model):
    CATEGORY = (
        ("Candy", "Candy"),
        ("Chocolate", "Chocolate"),
        ("Gift box", "Gift box"),
        ("Chocolate bar", "Chocolate bar"),
    )
    name = models.CharField(max_length=200, null=True)
    product_num = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200, null=True)
    category = models.CharField(max_length=200, null=True, choices = CATEGORY)
    price = models.FloatField(null = True)
    date_created=models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag, blank = True)
    rewards = models.IntegerField(null = True)

    def __str__(self):
        result = str(self.name) + " #" + str(self.product_num) #adding str infront of self.name because name could be null which could give error
        return result


class Order(models.Model):
    STATUS = (
        ("Pending", "Pending"),
        ("Fulfilled", "Fulfilled"),
        ("Delivered","Delivered"),
    )
    #related_name allows us to access the backward relationship so from Order to Customer, so we can now access all the Orders attributes from customer
    customer = models.ForeignKey(Customer, null = True, on_delete = models.SET_NULL, related_name = 'orders') 
    #product = models.ForeignKey(Product, null = True, on_delete = models.SET_NULL)
    order_items = models.ManyToManyField("OrderItem")
    note = models.CharField(max_length= 300, null = True, blank = True)
    date_created=models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length = 200, null = True, choices = STATUS)

    def __str__(self):
        result = "O" + str(self.id) + " - " + str(self.customer.name)
        return result
    
#stores the relationship between Order and Product
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        result = str(str(self.product)) + " - " + str(self.quantity)
        return result
