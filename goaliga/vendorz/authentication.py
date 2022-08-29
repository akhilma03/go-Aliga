import jwt,datetime
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication,get_authorization_header
from .models import Registrationz
from rest_framework.response import Response
from rest_framework import status, exceptions,generics


def create_access_token(id):
    return jwt.encode({
          #payload
          'vendor_id':id ,
          'exp': datetime.datetime.utcnow() +datetime.timedelta(seconds=30),
          'iat':datetime.datetime.utcnow()
    },'access_secret',algorithm='HS256')

def create_refresh_token(id):
    return jwt.encode({
          #payload
          'vendor_id':id ,
          'exp': datetime.datetime.utcnow()+datetime.timedelta(days=7),
          'iat':datetime.datetime.utcnow()
    },'refresh_secret',algorithm='HS256')



def decode_access_token (token):
      try:
        payload = jwt.decode(token,'access_secret',algorithms='HS256')
        return payload ['vendor_id']
      except Exception as e: 
        print (e)
        raise exceptions.AuthenticationFailed('unauthenticated')

def decode_refresh_token (token):
      try:
        payload = jwt.decode(token,'refresh_secret',algorithms='HS256')
        return payload ['vendor_id']
      except : 
        raise exceptions.AuthenticationFailed('unauthenticated')
# MIDDLEWARE
class StaffAuthentication(BaseAuthentication):
        def authenticate(self, request):

              auth = get_authorization_header(request).split()

              if auth and len(auth) == 2:
                    token = auth[1].decode('utf-8')
                    id =decode_access_token(token)
                    vendor = Registrationz.objects.get(pk=id)

                  #   user = Account.objects.filter(is_admin=True)
                    if vendor.is_staff:
                        return (vendor,None)

                    
              raise exceptions.AuthenticationFailed('unauthenticated')


# class AdminJwt(BaseAuthentication):
#         def authenticate(self, request):

#               auth = get_authorization_header(request).split()

#               if auth and len(auth) == 2:
#                     token = auth[1].decode('utf-8')
#                     id =decode_access_token(token)
#                     user = Registrationz.objects.get(pk=id)
#                     if user.is_admin:
#                          return (user,None)

#               raise exceptions.AuthenticationFailed('You have no permission')              



        







     