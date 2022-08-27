from multiprocessing import AuthenticationError
from urllib import request, response
from django.shortcuts import render

from .serializers import VendorSerilaizer,PackageSerilaizerz,CategorySerilaizer,ItinerarySerilaizer
from .models import Registrationz
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import exceptions
import jwt ,datetime
from trips.models import Packages,Itinerary,Category
from rest_framework import viewsets

from vendorz import serializers



# Create your views here.
@api_view(['POST'])
def RegisterVendor(request):
    data = request.data

    vendor = Registrationz.objects.create(
        company_name= data['company_name'],
        company_logo=data['company_logo'],
        adhar_no=data['adhar_no'],
        aadhar_image=data['aadhar_image'],
        office_address=data['office_address'],
        mobile=data['mobile'],
        email=data['email'],
        registration_doc=data['registration_doc'],
        licence_no=data['licence_no'],
        licence_image=data['licence_image'],
        year_of_experience=data['year_of_experience'],
        password=make_password(data['password']),
        confirm_password=make_password(data['password']))

    serializer = VendorSerilaizer(vendor,many = False)
    return Response(serializer.data)


class LoginView(APIView):
    def post(self,request):
        
        email = request.data['email']
        password = request.data['password']

        vendor = Registrationz.objects.filter(email=email,password=password).first()
        if vendor is None:
            raise exceptions.AuthenticationFailed ('No Vendor available')

        payload={
            'id':vendor.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=50),
            'iat':datetime.datetime.utcnow()


        }   
        token = jwt.encode(payload,'secret',algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt',value=token,httponly=True)

        response.data =({
            'jwt':token
        }) 

        return  response   

  



class ViewRegs(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
         token = request.COOKIES.get('jwt')

         if not token:
            raise exceptions.AuthenticationFailed ('Authentication Failed')
         try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

         except jwt.ExpiredSignatureError:
               raise exceptions.AuthenticationFailed ('Unauthenticated')

         vendor = Registrationz.objects.filter(id = payload['id']).first()
         serializer = VendorSerilaizer(vendor)
         return Response(serializer.data) 
    
class LogoutView(APIView):
    def post(self,request):
        response =Response()
        response.delete_cookie('jwt')
        response.data={
            'message':'success'
        }    
        return response

class ViewdetailRegs(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated]
    queryset = Registrationz.objects.all()
    serializer_class = VendorSerilaizer


    
class PackageViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset = Packages.objects.all()
    serializer_class = PackageSerilaizerz
   

class CategoryViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerilaizer


class ItineraryViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerilaizer