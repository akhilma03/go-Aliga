
from django.db import models
from accountz.models import Account
from trips.models import Packages

# Create your models here.


class PassengerDetails(models.Model):
    age = models.CharField(max_length=50)
    user =models.ForeignKey(Account,on_delete=models.CASCADE)
    name =models.CharField(max_length=500)
    address =models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    
class Order(models.Model):
    user =models.ForeignKey(Account,on_delete=models.CASCADE,null =True)
    order_package = models.ForeignKey(Packages,on_delete=models.CASCADE,null=True)
    order_amount = models.CharField(max_length=25)
    order_payment_id = models.CharField(max_length=100)
    isPaid = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True,null=True)
    address = models.ForeignKey(PassengerDetails,on_delete=models.CASCADE,null=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_status = models.BooleanField(default=True)
    
    def __str__(self):
        return self.order_package



