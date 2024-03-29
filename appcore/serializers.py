from django.contrib.auth.models import User
from .models import Bill,Payment,Tenant,PaymentRequest
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ('id','name','mobile_no','email','start_date','deposite','room_name','balance','active')

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id','date','amount')

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ('id','date','start_date','end_date','rent','units','price_per_unit','electric_total','water_bill','wifi_charge','total')

class PayRequestSerializer(serializers.ModelSerializer):
    tenant_name=serializers.CharField(source="tenant.name",read_only=True)
    class Meta:
        model=PaymentRequest
        fields=("id","img","amount","description","tenant","tenant_name")