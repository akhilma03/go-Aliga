from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from .models import Packages,Category,Itinerary,DateBooking,Variations


class ItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Itinerary
        fields = '__all__'    


class PackageSerilaizer(serializers.ModelSerializer):
    # itinerary= ItinerarySerializer(many=True,read_only=True)
    class Meta:
        model = Packages
        fields = ['package_name','slug','Overview','price','imagesMain','Days','category','No_of_peoples','inclusion','exclusion','things_to_pack']

# ['package_name','slug','Overview','price','imagesMain','Days','category','No_of_peoples','inclusion','exclusion','things_to_pack']

class CategorySerilaizerz(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'   



class SlotSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = DateBooking
        fields = '__all__'

class VariatiomSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Variations
        fields = '__all__'

