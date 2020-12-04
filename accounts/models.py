from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.core.mail import EmailMessage
# from django.contrib.sites.shortcuts import get_current_site

import string 
import random 
import threading
from django.template.defaultfilters import slugify

User._meta.get_field('email')._unique = True

class EmailThread(threading.Thread):

	def __init__(self,email):
		self.email=email
		threading.Thread.__init__(self)

	def run(self):
		self.email.send(fail_silently=False)

# Create your models here.
class Action_slugs(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    slug=models.SlugField(max_length=20,unique=True)
    forget=models.BooleanField(default=False)

@receiver(pre_save, sender=Action_slugs)
def create_slug(sender, instance, *args, **kwargs):
    res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 20))
    instance.slug=slugify(res)

class Owner(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    owner=models.BooleanField(default=False)

# Create your models here.
@receiver(post_save,sender=User)
def create_auth_token(sender,instance=None,created=False,**kwargs): #TOKEN activation slug generation with email verification
    if created:
        Token.objects.create(user=instance)

        
        activation_slug=Action_slugs(user=instance)
        activation_slug.save()

        domain="tenant-manager-arsenel.herokuapp.com"
        link="/account/user/action/"+str(activation_slug.slug)
        activate_url="https://"+domain+link
        subject="Email verification tenant"
        message="Hi "+str(instance.username)+"\n"+str(activate_url)+"\nIgnore(if not used Tenant arsenal(G)"
        to_list=[instance.email]
        email = EmailMessage(
                            subject,
                            message,
                            'gauravshinde696969@gmail.com',
                            to_list
                            )
        EmailThread(email).start()
        #commented for now to avoid sending emails



