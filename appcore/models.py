from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import pre_save,post_save,pre_delete
from django.dispatch import receiver
# Create your models here.

class Tenant(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    mobile_no=models.CharField(max_length=10)
    start_date=models.DateField(blank=True,null=True)
    deposite=models.IntegerField(blank=False)
    room_name=models.CharField(max_length=10)
    active=models.BooleanField(default=True)
    balance=models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Payment(models.Model):
    tenant=models.ForeignKey(Tenant,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    amount=models.IntegerField()

    def __str__(self):
        return str(self.date)

@receiver(post_save, sender=Payment)
def balance_payment(sender, instance, *args, **kwargs):
    tenant_instance=Tenant.objects.get(id=instance.tenant.id)
    tenant_instance.balance=tenant_instance.balance+instance.amount
    tenant_instance.save()

@receiver(pre_delete, sender=Payment)#objectionable
def balance_payment_delete(sender, instance, *args, **kwargs):
    tenant_instance=Tenant.objects.get(id=instance.tenant.id)
    tenant_instance.balance=tenant_instance.balance-instance.amount
    tenant_instance.save()


class Bill(models.Model):
    date=models.DateField(auto_now_add=True)
    tenant=models.ForeignKey(Tenant,on_delete=models.CASCADE)
    rent=models.IntegerField(default=0)
    units=models.IntegerField(default=0,blank=False,null=False)
    price_per_unit=models.IntegerField(default=0,blank=False,null=False)
    electric_total=models.IntegerField(default=0)
    water_bill=models.IntegerField(default=0)
    wifi_charge=models.IntegerField(default=0)
    total=models.IntegerField(default=0)


@receiver(pre_save, sender=Bill)
def calculate_total_bill(sender, instance, *args, **kwargs):
    instance.electric_total=instance.units*instance.price_per_unit
    instance.total=instance.rent+instance.electric_total+instance.water_bill+instance.wifi_charge


@receiver(post_save, sender=Bill)
def balance_bill(sender, instance, *args, **kwargs):
    tenant_instance=Tenant.objects.get(id=instance.tenant.id)
    tenant_instance.balance=tenant_instance.balance-instance.total
    tenant_instance.save()

@receiver(pre_delete, sender=Bill)#objectionable
def balance_bill_delete(sender, instance, *args, **kwargs):
    tenant_instance=Tenant.objects.get(id=instance.tenant.id)
    tenant_instance.balance=tenant_instance.balance+instance.total
    tenant_instance.save()