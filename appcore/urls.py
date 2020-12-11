from django.contrib import admin
from django.urls import path,include

from appcore.views import (landing,tenant_views,bill_views,payment_views,edit_delete_tenant,delete_bill,delete_payment,api_view_html,check_tenant_html,tenant_status,tenant_bill,tenant_payment,tenant_exporter,paymentRequestCreate,request_list,approved,denied2)

app_name="appcore"
urlpatterns = [
    path('',landing,name="landing"),
    path('api',api_view_html,name="api"),
    path('tenant',check_tenant_html,name="tenant_stat"),

    #API LINKS
    # check tenant
    path('status',tenant_status),     #API
    path('bills/<int:id>',tenant_bill),  #API
    path('payments/<int:id>',tenant_payment), #API
    path('exporter/<int:id>',tenant_exporter),

    #TENANT
    path('tenant_views',tenant_views,name="tenant_views"),#LIST VIEW AND CREATE #tenant id
    path('tenant_views/<int:id>',edit_delete_tenant,name="edit_delete_tenant"),#edit delte tenant #tenant id
    path('payment_views/<int:id>',payment_views,name="payment_views"), #tenant id
    path('bill_views/<int:id>',bill_views,name="bill_views"), #tenant id
    path('bill_delete/<int:id>',delete_bill,name="bill_delete"),#bill id
    path('payment_delete/<int:id>',delete_payment,name="payment_delete"),#payment id

    #payment request
    path('paymentrequest/<int:id>',paymentRequestCreate,name="paymentrequest"),#payment id

    #payment request list
    path('paymentlist',request_list,name="requestlist"),#payment id

    #approved
    path('approved/<int:id>',approved,name="approved"),#approved
    #denied
    path('denied/<int:id>',denied2,name="denied"),#denied



]
