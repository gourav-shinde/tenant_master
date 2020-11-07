from django.contrib import admin
from django.urls import path,include
from .views import UserRecordView,registeration_view
from rest_framework.authtoken.views import obtain_auth_token

app_name="accounts"
urlpatterns = [
    path('user/', UserRecordView.as_view(), name='users'),
    path('user/register',registeration_view, name='register'),
    path('user/login',obtain_auth_token, name='login'),
    #user update
    #user active after email verification
    #password change
]

