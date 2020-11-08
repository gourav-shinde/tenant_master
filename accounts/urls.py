from django.contrib import admin
from django.urls import path,include
from .views import UserRecordView,registeration_view,user_action,create_pass_change_token
from rest_framework.authtoken.views import obtain_auth_token

app_name="accounts"
urlpatterns = [
    path('user/', UserRecordView.as_view(), name='users'),
    path('user/register',registeration_view, name='register'),
    path('user/login',obtain_auth_token, name='login'),
    #user update
    #password change request using API
    path('user/request',create_pass_change_token,name="create_password_request"),
    #user active after email verification and password change
    path('user/action/<slug:id>',user_action,name="action")
    
]

