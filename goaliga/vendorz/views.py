
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
from rest_framework.decorators import authentication_classes

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from accountz.authentication import *
from payment.models import Order


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
            user = Registrationz.objects.get(email__exact=email)
            print(user)

            #reset password mail

            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()

            message={f'detail':'email sented to  {email}'}
            return Response(message,status=status.HTTP_200_OK)

        else:
                message={'detail':'no account presented'}
                return Response(message,status=status.HTTP_400_BAD_REQUEST) 

        # else:
        #         message={'detail':'no account presented'}
        #         return Response(message,status=status.HTTP_400_BAD_REQUEST) 
@api_view(['POST'])
def resetpassword_validate(request, uidb64, token): 
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = Account._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            request.session['uid'] = uid
            message={'detail':'uid taken'}
            return Response(message,status=status.HTTP_200_OK)
        else:
            message={'detail':'no account presented'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def resetpassword(request):
    data = request.data
    print(data)
    create_password = data['create_password']     
    confirm_password = data['confirm_password'] 
    print(create_password)        

    if create_password == confirm_password:

        uid = request.session.get('uid')
        user = Account.objects.get(pk=uid)
        user.set_password(create_password)
        user.save()
        message={'message':'password reset successfully'}
        return Response(message,status=status.HTTP_200_OK)
    else:
            message={'message':'password not match'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)    




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

@api_view(['POST'])
@authentication_classes([StaffAuthentication])
def AddPack(request):
    data= request.data
    vendors = request.user
    cat=Category.objects.get(id=data['category'])
    print(data['category'])
    vendor = Packages.objects.create(
    package_name= data['package_name'],
    slug=data['slug'],
    Overview=data['Overview'],
    price=data['price'],
    imagesMain=data['imagesMain'],
    images1=data['images1'],
    images2=data['images2'],
    images3=data['images3'],
    Days=data['Days'],
    category=cat,
    No_of_peoples=data['No_of_peoples'],
    inclusion=data['inclusion'],
    exclusion=['exclusion'],
    things_to_pack=data['things_to_pack'],
    is_available=data['is_available'],
    stock=data['stock'],
    vendor=vendors,
   )
    serializer = PackageSerilaizerz(vendor,many = False)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([StaffAuthentication])   
def VendorPack(request):
    vendor= request.user
    pack = Packages.objects.filter(vendor=vendor)
    serilaizer = PackageSerilaizerz(pack,many= True)
    return Response(serilaizer.data)


    
class PackageViewset(viewsets.ModelViewSet):
    authentication_classes = [StaffAuthentication]
    queryset = Packages.objects.all()   
    serializer_class = PackageSerilaizerz
   

class CategoryViewset(viewsets.ModelViewSet):
    authentication_classes = [AdminJwt]
    queryset = Category.objects.all()
    serializer_class = CategorySerilaizer


class ItineraryViewset(viewsets.ModelViewSet):
    authentication_classes = [StaffAuthentication]
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerilaizer

@api_view(['GET'])
def Vendorrevenew(request):
    total_revenue =0
    order_without=Order.objects.exclude(order_status="Cancelled")
    print(order_without)
    for order in order_without:
        total_revenue +=int(order.order_amount)
    vendor_amount=total_revenue-(total_revenue*(10/100))
    print(vendor_amount,"iu")
    
    return Response(vendor_amount)

# def VendorPack(request,id):
#     vendor = request.vendor
#     pakage = Packages.objects.get()
    