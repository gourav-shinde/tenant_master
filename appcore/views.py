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

#email requirements
import threading
from django.core.mail import EmailMessage
# Create your views here.

class EmailThread(threading.Thread):

	def __init__(self,email):
		self.email=email
		threading.Thread.__init__(self)

	def run(self):
		self.email.send(fail_silently=False)

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
            obj=serializer.save()
            subject="Email Confirmation tenant"
            message="Hi, \nMr/Mrs "+obj.name+".This email is linked with your tenant account(ARSENEL).It has been registered by "+user.username+".  \nIgnore if not registered"
            to_list=[obj.email]
            email = EmailMessage(
                                subject,
                                message,
                                'gauravshinde696969@gmail.com',
                                to_list
                                )
            # EmailThread(email).start()
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
            obj=serializer.save()
            subject="Payment-"+str(obj.date)
            message="Hi, \nMr/Mrs "+tenant.name+".Your Payment of "+str(obj.amount)+" is acknowledged by "+user.username+".  \nIgnore if not registered"
            to_list=[tenant.email]
            email = EmailMessage(
                                subject,
                                message,
                                'gauravshinde696969@gmail.com',
                                to_list
                                )
            # EmailThread(email).start()
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
            obj=serializer.save()
            subject="Bill-"+str(obj.date)
            bill_body="\nRent: "+str(obj.rent)+"\nElectric bill: "+str(obj.units)+"*"+str(obj.price_per_unit)+" = "+str(obj.electric_total)+"\nWifi bill: "+str(obj.wifi_charge)+"\nWater bill :"+str(obj.water_bill)+"\nTotal :"+str(obj.total)
            message="Hi, \nMr/Mrs "+tenant.name+"\nBill is generated by "+user.username+bill_body+"  \nIgnore if not registered"
            to_list=[tenant.email]
            email = EmailMessage(
                                subject,
                                message,
                                'gauravshinde696969@gmail.com',
                                to_list
                                )
            # EmailThread(email).start()
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