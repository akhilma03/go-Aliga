from django.shortcuts import render

from accountz.models import Account
from.serializers import AccountSerilaizer,VerifySerilazer
from rest_framework.response import Response 
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view,permission_classes 
from rest_framework import status
from .verify import send,check
from . import verify
from rest_framework.views import APIView

from accountz import serializers

# Create your views here.
@api_view(['POST']) 
def Registerz(request):
    data = request.data
    try:
        password = data['password']
        confirm_password = data['confirm_password']
        if password == confirm_password:
            userpassword =password
        else:
            print("The password is Missmatch")

        user = Account.objects.create(
            first_name = data['first_name'],
            last_name =  data['last_name'],
            email= data['email'],
            phone= data['phone'],
            password = make_password(userpassword)
        )
        phone= data['phone']
        request.session['phone']=phone
        send(phone)
        serilaizer = AccountSerilaizer(user,many=False)
        return Response(serilaizer.data)    
    except:
        message = {'detail':'User with this email already exist'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST)     

# class VerifyOtp(APIView):
#     def post(self,request):
#         # try:
#         data = request.data
#         print(data,111111111111111)
#         serializer = VerifySerilazer(data=data)
#         if serializer.is_valid():
#             print('valid')
#             otp = serializer.data['code']
#             phone = serializer.data['phone']
#             print(otp,phone,2222222222222222222)
#             if verify.check(phone,otp):
#                 print('verified')
#                 user = Account.objects.get(phone=phone)
#                 user.is_active = True
#                 user.save()
#                 print('activated')
#                 return Response(serializer.data)  
#         return Response({'msg': 'not valid'})
#     # except:
        
#         message = {'detail':'User with this email already exist'}
#         return Response(message) 

@api_view(['POST']) 
def verification(request):
    try:
        data = request.data
        phone = request.session['phone']
        code = data['code']
        if check(phone,code):
            user = Account.objects.get(phone=phone)
            user.is_active = True
            user.save()
            serializer = VerifySerilazer(user,many=False)
            return Response(serializer.data)
        else:
            message = {'detail':'User with this email already exist'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)     

    except:
        message = {'detail':'User with this email already exist'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST)     
        
    
