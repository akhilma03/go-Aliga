
import re
from django.shortcuts import render

from .serializers import VendorSerilaizer,PackageSerilaizerz,CategorySerilaizer,ItinerarySerilaizer
from .models import Registrationz,VendorToken
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import exceptions
import jwt ,datetime
from trips.models import Packages,Itinerary,Category
from rest_framework import viewsets
from .authentication import *
from django.contrib.auth.hashers import check_password

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from accountz.authentication import *

from vendorz import serializers

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage





# Create your views here.
@api_view(['POST'])
def RegisterVendor(request):
    data = request.data    
    if data['email']=='' or data['company_name']=='' or data['owner_name']=='' or data['office_address']=='' or data['password']=='':
         message={'error':' fill the blanks'}
         return Response(message,status=status.HTTP_400_BAD_REQUEST)
    if data['password'] != data['confirm_password']:
            raise exceptions.AuthenticationFailed ('password incorrect')
    print(data)        

    vendor = Registrationz.objects.create(
        company_name= data['company_name'],
        company_logo=data['company_logo'],
        adhar_no=data['adhar_no'],
         owner_name=data['owner_name'],
        aadhar_image=data['aadhar_image'],
        office_address=data['office_address'],
        mobile=data['mobile'],
        email=data['email'],
        registration_doc=data['registration_doc'],
        licence_no=data['licence_no'],
        licence_image=data['licence_image'],
        year_of_experience=data['year_of_experience'],
        password=make_password(data['password']))

    print(vendor,"iam vendor")

    send_mail('heloooo ',
            'Thank You For Registering with us,Your Application is underprocess ',
            'aligadrm@gmail.com'
            ,[vendor.email]   
            ,fail_silently=False)
 

    serializer = VendorSerilaizer(vendor,many = False)
    return Response(serializer.data)


class LoginView(APIView):
    def post(self,request):
        
        email = request.data['email']
        password = request.data['password']
        vendor = Registrationz.objects.filter(email=email).first()
        passwords =vendor.password

        if vendor is None:
            raise exceptions.AuthenticationFailed ('No Vendor available')

        if  not check_password(password, passwords) :
            raise exceptions.AuthenticationFailed ('Password Inncorect')

        # vendor = authenticate(email=email, password=password)      
        if vendor.is_staff:
            access_token = create_access_token(vendor.id)
            refresh_token = create_refresh_token(vendor.id)
            print("hellooo")

            VendorToken.objects.create(
                vendor_id = vendor.id,
                token= refresh_token,
                expired_at =  datetime.datetime.utcnow()+datetime.timedelta(days=7),
            )

            response = Response()
            response.set_cookie(key='refresh_token',
                                value=refresh_token, httponly=True)
            response.data = {
                'token': access_token
            }

            return  response   
        else:
            raise exceptions.AuthenticationFailed ('You are not a Vendor')



class ForgotAPIV(APIView):
    def post(self,request):
        data = request.data
        print(data)
        email = data['email']
        if Registrationz.objects.filter(email=email).exists():
            vendor = Registrationz.objects.filter(email=email).first()
            print(vendor)
        return Response ({'msg'})
        #reset password mail

        #     current_site = get_current_site(request)
        #     mail_subject = 'Reset Your Password'
        #     message = render_to_string('vendorz/reset.html', {
        #         'vendor': vendor,
        #         'domain': current_site,
        #         'uid': urlsafe_base64_encode(force_bytes(vendor.pk)),
        #         'token': default_token_generator.make_token(vendor),
        #     })
        #     to_email = email
        #     send_email = EmailMessage(mail_subject,message,to=[to_email])
        #     send_email.send()

        #     message={f'detail':'email sented to  {email}'}
        #     return Response(message,status=status.HTTP_200_OK)

        # else:
        #         message={'detail':'no account presented'}
        #         return Response(message,status=status.HTTP_400_BAD_REQUEST) 

  



# class ViewRegs(APIView):
#     authentication_classes = [JWTAuthentication]
#     def get(self,request):
#          token = request.COOKIES.get('jwt')

#          if not token:
#             raise exceptions.AuthenticationFailed ('Authentication Failed')
#          try:
#             payload = jwt.decode(token, 'secret', algorithms=['HS256'])

#          except jwt.ExpiredSignatureError:
#                raise exceptions.AuthenticationFailed ('Unauthenticated')

#          vendor = Registrationz.objects.filter(id = payload['id']).first()
#          serializer = VendorSerilaizer(vendor)
#          return Response(serializer.data) 



    
class LogoutView(APIView):
    def post(self,request):
        response =Response()
        response.delete_cookie('jwt')
        response.data={
            'message':'success'
        }    
        return response



    
class PackageViewset(viewsets.ModelViewSet):
    authentication_classes = [StaffAuthentication]
    queryset = Packages.objects.all()   
    serializer_class = PackageSerilaizerz
   

class CategoryViewset(viewsets.ModelViewSet):
    authentication_classes = [StaffAuthentication]
    queryset = Category.objects.all()
    serializer_class = CategorySerilaizer


class ItineraryViewset(viewsets.ModelViewSet):
    authentication_classes = [StaffAuthentication]
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerilaizer


