from django.contrib import admin
from .models import Bill,Payment,Tenant,PaymentRequest
# Register your models here.
admin.site.register(Bill)
admin.site.register(Payment)
admin.site.register(Tenant)
admin.site.register(PaymentRequest)