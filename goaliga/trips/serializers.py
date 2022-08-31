from dataclasses import fields
from rest_framework import serializers
from .models import Packages,Category,Itinerary

class ItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Itinerary
        fields = '__all__'

class PackageSerilaizer(serializers.ModelSerializer):
    # itinerary= ItinerarySerializer(many=True,read_only=True)
    class Meta:
        model = Packages
        fields = ['package_name','slug','Overview','price','imagesMain','Days','category','No_of_peoples','inclusion','exclusion','things_to_pack']
    

class CategorySerilaizerz(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'   



