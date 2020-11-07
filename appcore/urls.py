from django.contrib import admin
from django.urls import path,include

from appcore.views import (landing,tenant_views,bill_views,payment_views,edit_delete_tenant,delete_bill,delete_payment)

app_name="appcore"
urlpatterns = [
    path('',landing,name="landing"),

    #API LINKS

    #TENANT
    path('tenant_views',tenant_views,name="tenant_views"),#LIST VIEW AND CREATE #tenant id
    path('tenant_views/<int:id>',edit_delete_tenant,name="edit_delete_tenant"),#edit delte tenant #tenant id
    path('payment_views/<int:id>',payment_views,name="payment_views"), #tenant id
    path('bill_views/<int:id>',bill_views,name="bill_views"), #tenant id
    path('bill_delete/<int:id>',delete_bill,name="bill_delete"),#bill id
    path('payment_delete/<int:id>',delete_payment,name="payment_delete"),#payment id

]
