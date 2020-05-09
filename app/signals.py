from django.contrib.auth.models import User
from django.db.models.signals import post_save 
from django.contrib.auth.models import Group
from .models import Customer

def customer_profile(sender, instance, created, **kwargs):

    if created:
        group = Group.objects.get(name = "customer")

        #Remember that the instance is the user in this case 
        instance.groups.add(group)
        #To Create the customer in the customer model once the user is registered referecing the Customer model 

        Customer.objects.create(
            user = instance,
            name = instance.username, 
            email = instance.email
            )

        print('Profile Created !')

post_save.connect(customer_profile, sender = User)