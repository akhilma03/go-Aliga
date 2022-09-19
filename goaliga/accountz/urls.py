from . import views
from .views import *


from django.urls import path,include

urlpatterns = [
    
    path('register/',views.Registerz),
    path('verify/',views.verification),
    path('login/',LoginView.as_view()),
    # path('user/',UserApiView.as_view()),
    path('refresh/',RefreshAPIView.as_view()),
    path('logout/',LogoutAPIView.as_view()),
    path('forgot/',ForgotAPI.as_view()),
    path('resetpassword_validate/<uidb64>/<token>',views.resetpassword_validate,name="resetpassword_validate"),
    path('resetpassword/',views.resetpassword),
    path ('users/<int:pk>/',ViewallUser.as_view()),
    path('statusreg/<int:pk>/',views.statusApplication.as_view()),
    path('viewreg/',ViewRegs.as_view(),name='viewreg'),
    path('viewregs/<int:pk>/',ViewdetailRegs.as_view(),name='viewreg'),
    #  path('viwreg/<int:pk>/',views.verification),
    path('userprofile/',views.UserProfile),
    path('blockvendor/<int:pk>/',views.BlockVendor),
    path('orders/',views.UserOrder,name='uorders'),
    path('ordersdetails/<int:id>/',views.Orderdetails,name='ordersd'),
    path('allorder/',views.Orders,name='orders'),
     path('cancel/<int:id>/',views.CancelOrder,name='corders'),


       

] 