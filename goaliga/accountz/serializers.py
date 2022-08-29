
from wsgiref.validate import validator
from rest_framework import serializers
from .models import Account
import re


def isNamevalid(first_name):
    if(re.match("^(?=.{1,40}$)[a-zA-Z]+(?:[-'\s][a-zA-Z]+)*$",first_name)==None):
        print(first_name)
        raise serializers.ValidationError("Invalid Name ")
    return first_name 


class AccountSerilaizer(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields =['first_name','last_name','password','email','phone']
        validators = [isNamevalid]

    # def validate_first_name(self,first_name):
    #     if(re.match("^[a-zA-Z]*$",first_name)==None):
    #         raise serializers.ValidationError("Invalid Name ")
    #     return first_name    


class VerifySerilazer(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields = ['is_active']
   
 