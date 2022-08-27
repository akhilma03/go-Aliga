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
# Create your views here.


class ViewPackages(generics.ListAPIView):
    queryset = Packages.objects.filter(is_approve=True)
    serializer_class = PackageSerilaizer

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



