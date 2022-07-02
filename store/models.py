from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    def imageUrl(self):
        try:
            url = self.image.url
        except:
            url = 'https://dummyimage.com/400x500'
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    def get_total_price(self):
        orderitems = self.orderitem_set.all()
        price = sum([float(item.get_total_price()) for item in orderitems])
        return price
    
    def get_total_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        return str(round(self.quantity * self.product.price, 2))
   

class DeliveryAddress(models.Model):
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        if self.address == 'digit':
            return self.email
        else:
            return self.address



