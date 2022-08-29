from . import views
from .views import *


from django.urls import path,include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('packagez',PackageViewset,basename='package')   
router.register('category',CategoryViewset,basename='category')
router.register('itenery',PackageViewset,basename='package')
urlpatterns = [
    
    path('accounts/',views.RegisterVendor,name='register'),
    path('viewreg/',ViewRegs.as_view(),name='viewreg'),
    path('viewregs/<int:pk>/',ViewdetailRegs.as_view(),name='viewreg'),
    path('vlogin/',LoginView.as_view(),name='register'),
    path('vlogout/',LogoutView.as_view(),name='register'),

    ]+router.urls
