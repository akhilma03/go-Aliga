from django.db import models

# Create your models here.
class Registrationz(models.Model):
    Process =(('Applied','Applied'),('Under_Process ','Under_Process' ,),('Rejected','Rejected',),('Approved','Approved',))
    company_name = models.CharField(max_length=500)
    company_logo = models.ImageField(upload_to = 'photos/vendor')
    owner_name = models.CharField(max_length=500)
    adhar_no = models.CharField(max_length=500)
    aadhar_image=  models.ImageField(upload_to = 'photos/vendor')
    office_address = models.TextField(max_length=1000)
    mobile = models.CharField(max_length=500)
    email =models.CharField(max_length=500)
    registration_doc= models.ImageField(upload_to = 'photos/vendor')
    licence_no = models.CharField(max_length=500)
    licence_image = models.ImageField(upload_to = 'photos/vendor')
    year_of_experience =  models.CharField(max_length=100)
    password =  models.CharField(max_length=100)
    appProcess =  models.CharField(max_length=100, choices=Process,null=True,default='Applied')
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    

    def __str__(self):
        return self.company_name

class VendorToken(models.Model):
    vendor_id = models.IntegerField()
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()