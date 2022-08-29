
from rest_framework import serializers
from .models import Account
import re
from vendorz.models import Registrationz

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
   
 
class VendorSerilaizers(serializers.ModelSerializer):

    confirm_password = serializers.CharField

    class Meta:
        model = Registrationz
        # fields = ['company_name','company_logo','owner_name','adhar_no','aadhar_image','office_address','mobile','email','registration_doc','licence_no','licence_image','year_of_experience','password','confirm_password']
        fields = ['company_name','owner_name','is_staff','is_active','appProcess']
      