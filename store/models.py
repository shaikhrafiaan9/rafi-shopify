from django.db import models
from django.contrib.auth.models import User
from django.contrib import auth
from django.urls import reverse
# Create your models here.



class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=200,null=True)
    email = models.EmailField(max_length=100,null=True)

    def __str__(self):
        return self.name




class Product(models.Model):
    name = models.CharField(max_length=200,null=True)
    club = models.CharField(max_length=200,blank=True,null=True)
    year = models.CharField(max_length=200,blank=True,null=True)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    digital = models.BooleanField(default=False,null=True,blank=True)
    image = models.ImageField(null=True,blank=True)
    description = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = '/static'+self.image.url
        except:
            url = ''
        return url

    def get_absolute_url(self):
        return reverse("store:product_detail",kwargs = {'pk':self.pk})

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=True)
    transaction_id = models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitem = self.orderitem_set.all()
        for i in orderitem:
            if i.product.digital == False:
                shipping = True

        return shipping

    @property
    def get_cart_total(self):
        orderitem = self.orderitem_set.all()
        total = sum( item.get_total for item in orderitem)
        return total

    @property
    def get_cart_item(self):
        orderitem = self.orderitem_set.all()
        total = sum( item.quantity for item in orderitem)
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    pincode = models.CharField(max_length=200,null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.city)
