from django.contrib import admin

from .models import Order,PassengerDetails

admin.site.register(Order)
admin.site.register(PassengerDetails)