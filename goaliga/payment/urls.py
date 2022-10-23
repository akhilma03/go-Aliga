from .views import *
from . import views


from django.urls import path
urlpatterns = [

    path('pay/', start_payment, name="payment"),
    path('payment/success/', handle_payment_success, name="payment_success"),
    path('payz/', views.temp_payment, name="payy"),
    path('statusz/', views.paymentstatus, name="status"),
    path('address/',views.DetailsPassenger,name ="address")
]