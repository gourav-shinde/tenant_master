from django.shortcuts import render

#models
from django.contrib.auth.models import User
from .models import Bill,Payment,Tenant,PaymentRequest
from .serializers import BillSerializer,TenantSerializer,PaymentSerializer,PayRequestSerializer
#restframework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.decorators import api_view,permission_classes

from accounts.models import Owner

#email requirements
import threading
from django.core.mail import EmailMessage
import datetime
#export excel
import xlwt
from django.http import HttpResponse
# Create your views here.

class EmailThread(threading.Thread):

	def __init__(self,email):
		self.email=email
		threading.Thread.__init__(self)

	def run(self):
		self.email.send(fail_silently=False)

def landing(request):
    return render(request,"landing.html",{})

def api_view_html(request):
    return render(request,"api.html",{})

def check_tenant_html(request):
    return render(request,"check_tenant.html",{})

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
            EmailThread(email).start()
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
            tenant=Tenant.objects.get(id=id)
            statement=""
            if tenant.balance>=0:
                statement="You have credit of Rupees "+str(tenant.balance)
            else:
                statement="You have to pay "+str(tenant.balance)
            subject="Payment-"+str(obj.date)
            message="Hi, \nMr/Mrs "+tenant.name+".Your Payment of "+str(obj.amount)+" is acknowledged by "+user.username+".  \n"+statement+"\n"+"Ignore if not registered"
            to_list=[tenant.email]
            email = EmailMessage(
                                subject,
                                message,
                                'gauravshinde696969@gmail.com',
                                to_list
                                )
            EmailThread(email).start()
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
    owner=Owner.objects.get(user=user)
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
            tenant=Tenant.objects.get(id=id)
            subject="Bill-"+str(obj.date)
            statement=""
            if tenant.balance>=0:
                statement="You have credit of Rupees "+str(tenant.balance)
            else:
                statement="You have to pay "+str(tenant.balance)
            bill_body="\nRent: "+str(obj.rent)+"\nElectric bill: "+str(obj.units)+"*"+str(obj.price_per_unit)+" = "+str(obj.electric_total)+"\nWifi bill: "+str(obj.wifi_charge)+"\nWater bill :"+str(obj.water_bill)+"\nTotal :"+str(obj.total)
            message="Hi, \nMr/Mrs "+tenant.name+"\nBill is generated by "+user.username+bill_body+"\n"+statement+"\nMerchant Payment link: "+str(owner.link)+"  \nIgnore if not registered"
            to_list=[tenant.email]
            email = EmailMessage(
                                subject,
                                message,
                                'gauravshinde696969@gmail.com',
                                to_list
                                )
            EmailThread(email).start()
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




# WEB VIEW TENANT


@api_view(['POST']) #Tenant Check status
def tenant_status(request,*args, **kwargs):
    data={}
    if len(request.POST["mobile_no"]) == 10:
        try:
            tenant=Tenant.objects.get(mobile_no=int(request.POST["mobile_no"]),email=request.POST['email'],start_date=request.POST["date"])
            serializer=TenantSerializer(tenant)
            data["tenant"]=serializer.data
        except:
            data["msg"]="No Such Tenant exists,check inputs"
        
    else:
        data={"msg":"length of mobile number"}

    return Response(data=data)


@api_view(['GET']) #Tenant Check status
def tenant_bill(request,id):
    tenant=Tenant.objects.get(id=id)
    bills=Bill.objects.filter(tenant=tenant)
    serializer=BillSerializer(bills,many=True)
    data={"bills":serializer.data}
    return Response(data)

@api_view(['GET']) #Tenant Check status
def tenant_payment(request,id):
    tenant=Tenant.objects.get(id=id)
    payments=Payment.objects.filter(tenant=tenant)
    serializer=PaymentSerializer(payments,many=True)
    data={"payments":serializer.data}
    return Response(data)



#excel
def tenant_exporter(request,id):
    tenant=Tenant.objects.get(id=id)
    bills=Bill.objects.filter(tenant=tenant)
    payments=Payment.objects.filter(tenant=tenant)
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition']='attachment;filename=Tenant_'+str(tenant.name)+'.xls'
    wb=xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('Bills')
    row_num=6
    font_style=xlwt.XFStyle()
    font_style.font.bold=True
    #tenant details
    ws.write(0,0,"Name",font_style)
    ws.write(0,1,str(tenant.name),font_style)
    ws.write(1,0,"Mobile",font_style)
    ws.write(1,1,str(tenant.mobile_no),font_style)
    ws.write(2,0,"date",font_style)
    ws.write(2,1,str(datetime.datetime.today()),font_style)
    ws.write(3,0,"balance",font_style)
    ws.write(3,1,str(tenant.balance),font_style)

    columns=['Date','From','To','Rent','units','Price per unit','electric total','wifi','water','total']

    for col_no in range(len(columns)):
        ws.write(row_num,col_no,columns[col_no],font_style)
    
    font_style.font.bold=False
    
    for row in bills:
        # print(row)
        row_num+=1
        ws.write(row_num,0,str(row.date),font_style)
        ws.write(row_num,1,str(row.start_date),font_style)
        ws.write(row_num,2,str(row.end_date),font_style)
        ws.write(row_num,3,str(row.rent),font_style)
        ws.write(row_num,4,str(row.units),font_style)
        ws.write(row_num,5,str(row.price_per_unit),font_style)
        ws.write(row_num,6,str(row.electric_total),font_style)
        ws.write(row_num,7,str(row.wifi_charge),font_style)
        ws.write(row_num,8,str(row.water_bill),font_style)
        ws.write(row_num,9,str(row.total),font_style)

    ws2=wb.add_sheet('Payments')
    row_num=1
    font_style.font.bold=True
    columns=['Datetime','Amount']
    for col_no in range(len(columns)):
        ws2.write(row_num,col_no,columns[col_no],font_style) 
    
    font_style.font.bold=False

    for row in payments:
        row_num+=1
        ws2.write(row_num,0,str(row.date),font_style)
        ws2.write(row_num,1,str(row.amount),font_style)


    wb.save(response)

    return response



    #take payment request
def paymentRequestCreate(request,id):
    if request.POST:
        tenant=Tenant.objects.get(id=id)
        print(request.POST)
        print(request.FILES)
        request_pay=PaymentRequest(tenant=tenant,amount=request.POST.get("amount"),description=request.POST.get("description"),img=request.FILES.get("rimg"))
        request_pay.save()
        return render(request,"success2.html",{"Title":"Request successful"})
    return render(request,"payment_request.html",{})



@api_view(['GET'])
@permission_classes([IsAuthenticated])#get request list
def request_list(request):
    tenant=Tenant.objects.filter(owner=request.user)
    payment_request_list=PaymentRequest.objects.filter(tenant__in=tenant)
    serializer=PayRequestSerializer(payment_request_list,many=True)

    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def approved(request,id):
    user=request.user
    request_pay=PaymentRequest.objects.get(id=id)
    ten_id=request_pay.tenant.id
    tenant=Tenant.objects.get(id=ten_id)
    obj=Payment(tenant=tenant,amount=request_pay.amount)
    obj.save()
    tenant=Tenant.objects.get(id=ten_id)
    statement=""
    if tenant.balance>=0:
        statement="You have credit of Rupees "+str(tenant.balance)
    else:
        statement="You have to pay "+str(tenant.balance)
    subject="Payment-"+str(obj.date)
    message="Hi, \nMr/Mrs "+tenant.name+".Your Payment of "+str(obj.amount)+" is acknowledged by "+user.username+".\n This was acknowledgement of your payment request  \n"+statement+"\n"+"Ignore if not registered"
    to_list=[tenant.email]
    email = EmailMessage(
                        subject,
                        message,
                        'gauravshinde696969@gmail.com',
                        to_list
                        )
    EmailThread(email).start()

    request_pay.delete()
    data={"success":"success"}

    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def denied2(request,id):
    user=request.user
    obj=PaymentRequest.objects.get(id=id)
    tenant=Tenant.objects.get(id=obj.tenant.id)
    
    subject="Payment Request Denied"
    message="Hi, \nMr/Mrs "+tenant.name+".Your Payment Request of "+str(obj.amount)+" is denied by "+user.username+".\n This was acknowledgement of your payment request  \nIgnore if not registered"
    to_list=[tenant.email]
    email = EmailMessage(
                        subject,
                        message,
                        'gauravshinde696969@gmail.com',
                        to_list
                        )
    EmailThread(email).start()

    obj.delete()
    data={"success":"success"}

    return Response(data)
