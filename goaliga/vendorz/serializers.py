
from csv import excel
from dataclasses import field
from pyexpat import model
from wsgiref.validate import validator
from rest_framework import serializers
from .models import Registrationz
from trips . models import Packages
from trips.models import Packages,Itinerary,Category


def vendordergValid(data):
    print(data)
    print("iam validator")

class VendorSerilaizer(serializers.ModelSerializer):

    confirm_password = serializers.CharField

    class Meta:
        model = Registrationz
        # fields = ['company_name','company_logo','owner_name','adhar_no','aadhar_image','office_address','mobile','email','registration_doc','licence_no','licence_image','year_of_experience','password','confirm_password']
        fields = '__all__'
        extra_kwargs = {
            'password':{'write_only':True},
            # 'confirm_password':{'write_only':True}
        }
        validators=[vendordergValid]

class PackageSerilaizerz(serializers.ModelSerializer):
    class Meta:
        model = Packages
        exclude = ('availablity','is_approve','date','modified_date','created_date' )
        # ['package_name','slug','Overview','price','imagesMain','images1','images2','images3','Days','category','No_of_peoples','inclusion','exclusion','things_to_pack','is_available']

class ItinerarySerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Itinerary
        fields = '__all__'

class CategorySerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__' 


         