from django.shortcuts import render

#models
from django.contrib.auth.models import User
from .models import Bill,Payment,Tenant
from .serializers import BillSerializer,TenantSerializer,PaymentSerializer
#restframework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
# Create your views here.

def landing(request):
    return render(request,"landing.html",{})

#TENANTS
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def tenant_views(request):
    user=request.user
    if request.method=="GET":
        tenants=Tenant.objects.filter(owner=user)
        serializer=TenantSerializer(tenants,many=True)
        data={"tenants":serializer.data}
        return Response(data)
    if request.method=="POST":
        tenant=Tenant(owner=user)
        serializer=TenantSerializer(tenant,data=request.data)
        data={}
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




@api_view(['PUT','DELETE']) #DELETE and UPDATE
@permission_classes([IsAuthenticated])
def edit_delete_tenant(request,id):
    user=request.user
    try:
        tenant=Tenant.objects.get(id=id)
    except Tenant.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method=="PUT":
        serializer=TenantSerializer(tenant,data=request.data)
        data={}
        if serializer.is_valid():
            serializer.save()
            data["success"]="update successful"
            return Response(data=data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    if request.method=="DELETE":
        operation=tenant.delete()
        data={}
        if operation:
            data["success"]="delete successful"
        else:
            data["failure"]="delete failed"
        return Response(data=data)


#PAYMENTS
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])#detailed list of payments
def payment_views(request,id):
    user=request.user
    tenant=Tenant.objects.get(id=id)
    if request.method=="GET":
        payments=Payment.objects.filter(tenant=tenant)
        serializer=PaymentSerializer(payments,many=True)
        data={"payments":serializer.data}
        return Response(data)
    if request.method=="POST":
        payment=Payment(tenant=tenant)
        serializer=PaymentSerializer(payment,data=request.data)
        data={}
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE']) #DELETE  PAYMENT
@permission_classes([IsAuthenticated])
def delete_payment(request,id):
    user=request.user
    try:
        payment=Payment.objects.get(id=id)
    except Tenant.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method=="DELETE":
        operation=payment.delete()
        data={}
        if operation:
            data["success"]="delete successful"
        else:
            data["failure"]="delete failed"
        return Response(data=data)

#BILLS
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])#detailed list of Bills
def bill_views(request,id):
    user=request.user
    tenant=Tenant.objects.get(id=id)
    if request.method=="GET":
        bills=Bill.objects.filter(tenant=tenant)
        serializer=BillSerializer(bills,many=True)
        data={"bills":serializer.data}
        return Response(data)
    if request.method=="POST":
        bill=Bill(tenant=tenant)
        serializer=BillSerializer(bill,data=request.data)
        data={}
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE']) #DELETE BILL
@permission_classes([IsAuthenticated])
def delete_bill(request,id):
    user=request.user
    try:
        bill=Bill.objects.get(id=id)
    except Tenant.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method=="DELETE":
        operation=bill.delete()
        data={}
        if operation:
            data["success"]="delete successful"
        else:
            data["failure"]="delete failed"
        return Response(data=data)