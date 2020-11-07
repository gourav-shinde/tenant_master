from django.contrib import admin
from .models import Bill,Payment,Tenant
# Register your models here.
admin.site.register(Bill)
admin.site.register(Payment)
admin.site.register(Tenant)