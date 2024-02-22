from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Products(models.Model):
    image=models.ImageField(upload_to="media")
    sname=models.CharField(max_length=50)
    quantity=models.CharField(max_length=50)
    price=models.IntegerField()
    description=models.CharField(max_length=500)

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.CharField(max_length=10,default="NA")
    def str(self):
        return self.user.username
    
class Cartitem(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=0)
    products=models.ForeignKey(Products,on_delete=models.CASCADE, null=True)
    class Meta:
        db_table='cart_items'
    def str(self):
        return self.products.name
    
class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    building_name=models.CharField(max_length=200,null=False)
    street=models.CharField(max_length=200,null=False)
    landmark=models.CharField(max_length=200,blank=True,null=True)
    city=models.CharField(max_length=200,blank=True,null=True)
    state=models.CharField(max_length=30,null=False)
    zipcode=models.CharField(max_length=6,null=False)
    date_added=models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transation_id = models.CharField(max_length=100, null=False)
    shipping_address = models.ForeignKey(
        ShippingAddress, on_delete=models.CASCADE, null=True)

    def _str_(self):
        return str(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItems(models.Model):
    product=models.ForeignKey(Products,on_delete=models.SET_NULL,null=True)
    order=models.ForeignKey(Order,related_name='items',on_delete=models.SET_NULL,null=True)
    quantity=models.IntegerField(default=9,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)

    def get_cost(self):
        return self.price * self.quantity
