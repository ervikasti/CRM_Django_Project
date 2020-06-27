from django.db.models.signals import post_save
from django.contrib.auth.models import User,Group
from.models import Customer

def customer_profile(sender, instance, created,**kwargs):
    if created:
        #adding register user to customer group
        group = Group.objects.get(name='customer')
        #print(group)
        instance.groups.add(group)
        #youtube vedio no pt16.adding regis to user 
        Customer.objects.create(
            user = instance,
            name = instance.username,
            email = instance.email,
        )

post_save.connect(customer_profile,sender =User)