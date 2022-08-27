from dataclasses import fields
from rest_framework import serializers
from .models import Packages

class PackageSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Packages
        fields = ['package_name','slug','Overview','price','imagesMain','Days','category','No_of_peoples','inclusion','exclusion','things_to_pack']
    
