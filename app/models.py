from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone

from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank = True, on_delete = models.CASCADE)
    name = models.CharField(max_length = 200, null = True)
    email = models.CharField(max_length = 200, null = True)
    contact = PhoneNumberField(null = True)
    profile_pic = models.ImageField(default="icon4.jpg",null = True, blank = True)
    date_created = models.DateTimeField(default = timezone.now, null=True)


    def __str__(self):
        return self.name or ''

        
class Product(models.Model):
    #Choices for Category selection in a tuple
    CATEGORY = (
        ('Phones', 'Phoness'),
        ('Books', 'Books'),
        ('Fashion', 'Fashion'),
        ('Technology Gadgets','Technology Gadgets'),
        ('Electronics', 'Electronics'),
        
    )

    name = models.CharField(max_length = 300, null = True)
    price = models.FloatField(null = True)
    category = models.CharField(max_length = 200, null=True, choices = CATEGORY)
    description = models.TextField(max_length = 300, null = True)
    date_created = models.DateTimeField(default = timezone.now)
 

    def __str__(self):
        return self.name



class Order(models.Model):

    #Choices for the Status in a Tuple

    STATUS = (
        ('Delivered', 'Delivered'),
        ('Out for Delivery' , 'Out for Delivery'),
        ('Pending', 'Pending')
    )

    customer = models.ForeignKey(Customer, null = True, on_delete = models.SET_NULL)
    product = models.ForeignKey(Product, null = True, on_delete = models.SET_NULL)
    status = models.CharField(max_length = 200, null=True, choices = STATUS)
    date_created = models.DateTimeField(default = timezone.now)

    def __str__(self):

        return "{} - {}".format(self.customer, self.product)
    



















































































 