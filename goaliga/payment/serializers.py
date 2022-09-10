from rest_framework import serializers

from .models import Order,PassengerDetails

class OrderSerializer(serializers.ModelSerializer):
    order_date = serializers.DateTimeField(format="%d %B %Y %I:%M %p")

    class Meta:
        model = Order
        fields = '__all__'
        depth = 2
        
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassengerDetails
        fields = '__all__'         