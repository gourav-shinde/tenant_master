from django.test import TestCase,SimpleTestCase,Client
from rest_framework.test import APIClient
from rest_framework.test import APITestCase, URLPatternsTestCase
from django.contrib.auth.models import User
from .models import Tenant,Bill,Payment
from .views import landing,check_tenant_html,api_view_html
from django.urls import reverse,resolve

from requests.auth import HTTPBasicAuth

import json
# Create your tests here.


#testing webpages
class Testurls(SimpleTestCase):

    def test_landing_url(self):
        url=reverse('landing')
        self.assertEquals(resolve(url).func,landing)

    def test_api_view_url(self):
        url=reverse('appcore:api')
        self.assertEquals(resolve(url).func,api_view_html)

    def test_tenant_url(self):
        url=reverse('appcore:tenant_stat')
        self.assertEquals(resolve(url).func,check_tenant_html)


class TestViews(TestCase):

    def test_tenant_get(self):
        client=APIClient()
        user=User(username="admin")
        client.force_authenticate(user=user)
        response=client.get(reverse('appcore:tenant_views'))
        self.assertEquals(response.status_code,200)


    def test_payment_get(self):
        client=APIClient()

        user=User(username="admin")
        account=User(
            email="gauravsanjayshinde@gmail.com",
            username="self.validated_data['username']",
        )
        account.set_password("G123456789")
        account.save()

        Tenant.objects.create(owner=account,name="olaa",mobile_no=9876543210,email="gauravsanjayshinde@gmail.com",start_date="2020-12-08",deposite=1000,room_name="isto")
        tenant=Tenant.objects.get(name="olaa")
        client.force_authenticate(user=user)
        self.assertEquals(tenant.id,1)
        response=client.get("http://127.0.0.1:8000/app/payment_views/1")
        self.assertEquals(response.status_code,200)

    def test_bill_get(self):
        client=APIClient()
        user=User(username="admin")
        client.force_authenticate(user=user)

        account=User(
            email="gauravsanjayshinde@gmail.com",
            username="self.validated_data['username']",
        )
        account.set_password("G123456789")
        account.save()

        Tenant.objects.create(owner=account,name="olaa",mobile_no=9876543210,email="gauravsanjayshinde@gmail.com",start_date="2020-12-08",deposite=1000,room_name="isto")
        tenant=Tenant.objects.get(name="olaa")

        self.assertEquals(tenant.id,1)
        response=client.get("http://127.0.0.1:8000/app/bill_views/1")
        self.assertEquals(response.status_code,200)

    def test_tenant_post(self):
        client=APIClient()
        user=User(username="admin")
        

        account=User(
            email="gauravsanjayshinde@gmail.com",
            username="self.validated_data['username']",
        )
        account.set_password("G123456789")
        account.save()
        client.force_authenticate(user=account)

        response=client.post("http://127.0.0.1:8000/app/tenant_views",json={"name":"olaa1","mobile_no":9876543210,"deposite":100,"room_name":"hello"})
        self.assertEquals(response.status_code,400)