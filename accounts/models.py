from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
User._meta.get_field('email')._unique = True
User._meta.get_field('email')._required = True
# Create your models here.

class Owner(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    owner=models.BooleanField(default=False)

# Create your models here.
@receiver(post_save,sender=User)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)