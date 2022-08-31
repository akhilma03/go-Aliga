from django.db import models

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
    Overview         = models.TextField(max_length=1000,blank = True)
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
    inclusion        = models.TextField(max_length=500)   
    exclusion        = models.TextField(max_length=500) 
    things_to_pack   = models.TextField(max_length=500) 
    is_approve       = models.BooleanField(default=False)
    is_available     = models.BooleanField(default=True)
    location         = models.CharField(max_length=100,null=True)
    date             = models.DateField(null=True)
    availablity      =  models.CharField(max_length=100,null=True)


    
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
    Date=models.CharField(max_length=50)
    days=models.CharField(max_length=30)
    active=models.BooleanField(default=False)

    def __str__(self):
        return self.days