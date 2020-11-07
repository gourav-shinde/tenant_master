from .serializers import UserSerializer,RegisterationSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User

from django.shortcuts import render

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

    else:
        data=serializer.errors
    return Response(data)
