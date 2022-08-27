from . import views
from .views import *


from django.urls import path,include

urlpatterns = [
    
    path('register/',views.Registerz),
    path('verify/',views.verification),
    path('login/',LoginView.as_view()),
    path('user/',UserApiView.as_view()),
    path('refresh/',RefreshAPIView.as_view()),
    path('logout/',LogoutAPIView.as_view()),
    path('forgot/',ForgotAPI.as_view()),
    path('resetpassword_validate/<uidb64>/<token>',views.resetpassword_validate,name="resetpassword_validate"),
     path('resetpassword/',views.resetpassword),
     path ('users/',ViewallUser.as_view()),
   
] 