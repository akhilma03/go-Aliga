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
    path('vlogin/',LoginView.as_view(),name='register'),
    path('vlogout/',LogoutView.as_view(),name='register'),
    path('vforgot/',ForgotAPIV.as_view(),name='vforgot'),
    path('revenew/',views.Vendorrevenew),
    path('addpack/',views.AddPack),
    path('vendorpack/',views.VendorPack),
    path('resetpassword_validate/<uidb64>/<token>',views.resetpassword_validate,name="resetpassword_validate"),
    path('resetpassword/',views.resetpassword),

    ]+router.urls
