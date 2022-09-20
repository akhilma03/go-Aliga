from . import views
from .views import *


from django.urls import path

urlpatterns = [
    
    path('',views.index),
    path('<str:room_name>/',views.room),
    ]