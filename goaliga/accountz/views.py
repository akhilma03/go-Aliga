
from email import header
from lib2to3.pgen2 import token
from os import access
from . authentication import create_access_token, create_refresh_token
from .verify import send, check
from rest_framework import status, exceptions
from rest_framework.response import Response
from accountz import serializers
from rest_framework.authentication import get_authorization_header
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from accountz.models import Account,UserToken
from .serializers import AccountSerilaizer, VerifySerilazer
from rest_framework.decorators import api_view, permission_classes
from .authentication import *


# Create your views here.
@api_view(['POST'])
def Registerz(request):
    data = request.data
    try:
        password = data['password']
        confirm_password = data['confirm_password']
        if password == confirm_password:
            userpassword = password
        else:
            print("The password is Missmatch")

        user = Account.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data['phone'],
            password=make_password(userpassword)
        )
        phone = data['phone']
        request.session['phone'] = phone
        send(phone)
        serilaizer = AccountSerilaizer(user, many=False)
        return Response(serilaizer.data)
    except:
        message = {'detail': 'User with this email already exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

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
        if check(phone, code):
            user = Account.objects.get(phone=phone)
            user.is_active = True
            user.save()
            serializer=AccountSerilaizer(user,many=False)
            return Response(serializer.data)
        else:
            message={'detail':'otp is not valid'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)    
    except:
        message={'detail':'error in serializer'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST)
    


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = Account.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed('Invalid Credientials')

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Invalid Credientials')

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        UserToken.objects.create(
            user_id = user.id,
            token= refresh_token,
            expired_at =  datetime.datetime.utcnow()+datetime.timedelta(days=7),
        )

        response = Response()
        response.set_cookie(key='refresh_token',
                            value=refresh_token, httponly=True)
        response.data = {
            'token': access_token
        }

        return response


class UserApiView(APIView):

    authentication_classes = [JWTAuthentication]
    def get(self, request):
            return Response(AccountSerilaizer(request.user).data)


class RefreshAPIView(APIView):
    def post(self,request):
        refresh_token = request.COOKIES.get('refresh_token')
        id = decode_refresh_token(refresh_token)

        if not UserToken.objects.filter(user_id = id,
        token = refresh_token,expired_at__gt=datetime.datetime.now(tz=datetime.timezone.utc)).exists():
             raise exceptions.AuthenticationFailed('unautherozied') 
       
        access_token = create_access_token(id)
        return Response ( {
            'token': access_token
        })  


class LogoutAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    def post(self,request):
        UserToken.objects.filter(user_id= request.user.id).delete()
        response = Response()
        response.delete_cookie(key='refresh_token')
        response.data = {
            'message':'success'
        }
        return response
