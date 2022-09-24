from ast import Pass
from email import message
from django.shortcuts import render
from rest_framework import generics
from accountz.authentication import *
from .serializers import *
from .models import *
from rest_framework.decorators import api_view
from django .shortcuts import get_list_or_404
from .serializers import *
from rest_framework.response import Response
from rest_framework import status 
import datetime
from  payment.models import Order,PassengerDetails
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .pagination import PackagePagination
from rest_framework import viewsets
from accountz.authentication import JWTAuthentication
# Create your views here.


class ViewPackages(generics.ListAPIView):
    queryset = Packages.objects.filter(is_available=True)
    serializer_class = PackageSerilaizer
    pagination_class = PackagePagination

#filter
class FilterPackages(generics.ListAPIView):
    queryset = Packages.objects.filter(is_available=True)
    serializer_class = PackageSerilaizer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['package_name','slug']

#search
class SearchPackages(generics.ListAPIView):
     queryset = Packages.objects.filter(is_available=True) 
     serializer_class = PackageSerilaizer
     filter_backends = [filters.SearchFilter]
     search_fields = ['slug','package_name','price','category__category_name']
#ordering
class OrderPackages(generics.ListAPIView):
     queryset = Packages.objects.filter(is_available=True) 
     serializer_class = PackageSerilaizer
     filter_backends = [filters.OrderingFilter]
     ordering = ['price','Days']

     
    

# class ViewPackages(generics.ListAPIView):
#     queryset = Packages.objects.filter(is_approve=True)
#     serializer_class = PackageSerilaizer

    # def get_queryset(self):
    #  package_name = self.request.query_params.get('package_name',None)
    #  return Packages.objects.filter(package_name=package_name)
    

@api_view(['GET'])
def trips(request,category_slug):
    categories = None
    packages = None
    try:
        if category_slug is not None:
            # categories = get_list_or_404(Category,slug = category_slug)
            categories=Category.objects.get(slug = category_slug)
            print(categories)
            package = Packages.objects.filter(category=categories)
            serializer = PackageSerilaizer(package ,many=True)

            return Response(serializer.data) 

    except:
        package = Packages.objects.all()
    message = {'detail':'Package is not available'}

    return Response(message,status=status.HTTP_400_BAD_REQUEST) 
              
@api_view(['GET'])
def tripdetails(request,category_slug,package_slug):
    try:
        single_package = Packages.objects.get(category__slug=category_slug,slug=package_slug)
        serializer = PackageSerilaizer(single_package ,many=False)
        return Response(serializer.data) 
    except:
        message = {'detail':'No Package is  available'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST) 


@api_view(['GET'])
def viewCat(request):
    categories = Category.objects.all()
    serializer = CategorySerilaizerz(categories,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def Bookuser(request,pk):
    now = datetime.datetime.now()
    print(now)
    package = Packages.objects.get(id=pk)
    slot = DateBooking.objects.filter(package=package,Date__gte=now)
    serializer = SlotSerilaizer(slot,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def AddBook(request):
    serializer = SlotSerilaizer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)    



@api_view(['GET'])
def addVariation(request,pk):
    package = Packages.objects.get(id=pk)
    variation = Variations.objects.filter(package=package)
    serializer = SlotSerilaizer(variation,many=True)
    return Response(serializer.data)


authentication_classes = [JWTAuthentication]
class Reviews(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class =ReviewSerializer


# class Reviews(generics.ListCreateAPIView):
#     # queryset = Review.objects.all()
#     serializer_class =ReviewSerializer

#     def get_queryset(self):
#         pk = self.kwargs['pk']
#         return Review.objects.filter(package=pk)
       

