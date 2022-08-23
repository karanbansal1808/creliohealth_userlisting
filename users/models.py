from distutils.command import upload
from queue import Empty
from django.db import models

# Create your models here.
class Userdetails(models.Model):
    name=models.CharField(max_length=255)
    gender=models.CharField(max_length=255,default="Other")
    location=models.TextField(null=True)
    email=models.TextField(null=True)
    dob=models.DateField(null=True)
    phone=models.TextField(null=True)
    cell=models.TextField(null=True)
    id=models.TextField(null=True)
    nationality=models.CharField(max_length=255,null=True)
    picture=models.ImageField(null=True)
    registered=models.TextField(null=True)
    username=models.TextField(null=True)
    uuid=models.CharField(primary_key=True,max_length=255,default=0)
    city=models.TextField(null=True)
    state=models.TextField(null=True)
    country=models.TextField(null=True)
    postcode=models.TextField(null=True)
    
    
    
    
    


