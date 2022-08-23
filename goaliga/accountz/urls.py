from . import views
from .views import *


from django.urls import path,include

urlpatterns = [
    
    path('register/',views.Registerz),
    path('verify/',views.verification),
    path('login/',LoginView.as_view()),
    path('user/',UserApiView.as_view()),
    path('refresh/',RefreshAPIView.as_view()),
    path('logout/',LogoutAPIView.as_view())


] 