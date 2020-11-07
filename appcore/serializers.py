from django.contrib.auth.models import User
from .models import Bill,Payment,Tenant
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ('id','name','mobile_no','start_date','deposite','room_name','balance')

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id','date','amount')

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ('id','date','rent','electric_total','water_bill','wifi_charge','total')
