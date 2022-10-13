
from django.db import models

from django.core.validators import MinValueValidator,MaxValueValidator
from vendorz.models import Registrationz
from accountz . models import  Account

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50,unique=True)                                                                                                                    
    slug = models.SlugField(max_length=50,unique=True)
    description = models.CharField(max_length=300,blank=True)
    images = models.ImageField(upload_to ='photos/categories',blank =True)

    def __str__(self):
        return self.category_name

class Packages(models.Model):
    package_name     = models.CharField(max_length=100,unique=True)
    slug             = models.SlugField(max_length=100,unique=True)
    Overview         = models.TextField(max_length=3000,blank = True)
    price            = models.IntegerField()
    imagesMain       = models.ImageField(upload_to = 'photos/product')
    images1          = models.ImageField(upload_to = 'photos/product')
    images2          = models.ImageField(upload_to = 'photos/product')
    images3          = models.ImageField(upload_to = 'photos/product')
    Days             = models.CharField(max_length=100)
    is_available     = models.BooleanField(default=True)
    category         = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date     = models.DateTimeField(auto_now_add=True)
    modified_date    = models.DateTimeField(auto_now=True)
    No_of_peoples    = models.CharField(max_length=100)
    inclusion        = models.TextField(max_length=2000)   
    exclusion        = models.TextField(max_length=1000) 
    things_to_pack   = models.TextField(max_length=2000) 
    is_approve       = models.BooleanField(default=False)
    is_available     = models.BooleanField(default=True)
    location         = models.CharField(max_length=100,null=True)
    date             = models.DateField(auto_now_add=True, null=True)
    availablity      =  models.CharField(max_length=100,null=True)
    stock           = models.IntegerField(null=True)
    vendor          = models.ForeignKey(Registrationz,on_delete=models.CASCADE,null=True)

    
    def __str__(self):
        return self.package_name


class Itinerary(models.Model):
    package = models.ForeignKey(Packages,on_delete=models.CASCADE,related_name="itinerary")
    itinerary_name = models.CharField(max_length=100)
    days = models.CharField(max_length=165)
    description = models.TextField(max_length=500)
   
    def __str__(self):
        return self.itinerary_name


class DateBooking(models.Model):
    package=models.ForeignKey(Packages,on_delete=models.CASCADE,null=True,blank=True)   
    Date=models.DateField(blank=True)
    days=models.CharField(max_length=30)
    count = models.IntegerField(null=True)
    active=models.BooleanField(default=False)
    isbooked = models.BooleanField(default=False,blank=True)
     

    def __str__(self):
        return self.package.package_name

variation_choice =(('No_of_peoples','No_of_peoples'),('No_Days','No Days'))
class Variations(models.Model):
    package = models.ForeignKey(Packages,on_delete=models.CASCADE)
    variation_category =models.CharField(max_length=100,choices=variation_choice)
    variation_value = models.IntegerField() 
    is_active = models.BooleanField(default=True)
     


    def __str__(self):

        return self.variation_category  


 


class Review(models.Model):
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    description = models.CharField(max_length=200,null=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    package = models.ForeignKey(Packages,on_delete=models.CASCADE,related_name="reviews")

    def __str__(self) :
        return str(self.rating)+" - "+self.package.package_name


class Favourites(models.Model):
    package = models.ForeignKey(Packages,on_delete=models.CASCADE,null=True,blank=True)   
    user    = models.ForeignKey(Account,on_delete=models.CASCADE,null=True,blank=True)   
    isfav =  models.BooleanField(default=True)