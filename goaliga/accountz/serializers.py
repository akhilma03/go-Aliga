
from rest_framework import serializers
from .models import Account

class AccountSerilaizer(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields =['first_name','last_name','password','email','phone']


class VerifySerilazer(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields = ['is_active']
   