from .serializers import UserSerializer,RegisterationSerializer,EmailSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
#models
from django.contrib.auth.models import User
from .models import Action_slugs

#forms
from .forms import Register_Form

from django.shortcuts import render
from django.core.mail import EmailMessage
import threading

class EmailThread(threading.Thread):

	def __init__(self,email):
		self.email=email
		threading.Thread.__init__(self)

	def run(self):
		self.email.send(fail_silently=False)

class UserRecordView(APIView):
    """
    API View to create or get a list of all the registered
    users. GET request returns the registered users whereas
    a POST request allows to create a new user.
    """
    permission_classes = [IsAdminUser]

    def get(self, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "error": True,
                "error_msg": serializer.error_messages,
            },
            status=status.HTTP_400_BAD_REQUEST
        )


#REGISTERATION VIEW
@api_view(['POST',])
def registeration_view(request):
    serializer=RegisterationSerializer(data=request.data)
    data={}
    if serializer.is_valid():
        account=serializer.save()
        data['response']="Successfully Registered"
        data['email']=account.email
        data['username']=account.username
        token=Token.objects.get(user=account).key
        data['token']=token
        return Response(data)
    else:
        data=serializer.errors
        return Response(data,status=400)


def user_action(request,id):
    action=Action_slugs.objects.get(slug=id)
    user=User.objects.get(id=action.user.id)
    if action.forget==False:
        user.is_active=True
        user.save()
        action.delete()
        return render(request,"activation.html",{})
    else:
        
        form=Register_Form(request.POST or None)
        if form.is_valid():
            password=form.save(commit=False)
            user.set_password(request.POST.get('password1'))
            user.save()
            action.delete()
            return render(request,"success.html",{"Title":"Password Changed"})
        return render(request,"change_password.html",{"form":form,"email":user.email,"username":user.username})
    try:
        pass
    except:
        return render(request,"success.html",{"Title":"Something went Wrong"})

@api_view(['POST',])
def create_pass_change_token(request):
    serializer=EmailSerializer(data=request.data)
    data={}
    if serializer.is_valid():
        email=serializer.data['email']
        try:
            user=User.objects.get(email=email)
            passwordtoken=Action_slugs(user=user,forget=True)
            passwordtoken.save()

            domain="tenant-manager-arsenel.herokuapp.com"
            link="/account/user/action/"+str(passwordtoken.slug)
            activate_url="https://"+domain+link
            subject="Password Change link - tenant"
            message="Hi "+str(user.username)+"\n"+str(activate_url)+"\nIgnore(if not used Tenant arsenal(G)"
            to_list=[user.email]
            email = EmailMessage(
                                subject,
                                message,
                                'gauravshinde696969@gmail.com',
                                to_list
                                )
            EmailThread(email).start()
            data["status"]="Success!!Email Sent"

        except user.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        data=serializer.errors
    return Response(data)

@api_view(['POST',])
def requestUsername(request):
    serializer=EmailSerializer(data=request.data)
    data={}
    if serializer.is_valid():
        email=serializer.data['email']
        try:
            user=User.objects.get(email=email)
            domain="tenant-manager-arsenel.herokuapp.com"
            subject="Username -Tenant"
            message="Hi ,Your username is "+str(user.username)+"\n"+"\nIgnore(if not used Tenant arsenal(G)"
            to_list=[user.email]
            email = EmailMessage(
                                subject,
                                message,
                                'gauravshinde696969@gmail.com',
                                to_list
                                )
            EmailThread(email).start()
            data["status"]="Success!!Email Sent"

        except user.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        data=serializer.errors
    return Response(data)
