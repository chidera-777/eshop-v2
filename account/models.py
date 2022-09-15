from django.db import models
from django.conf import settings 
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, default=None)
    postal_code = models.CharField(max_length=12, default=None)
    country = models.CharField(max_length=50, default=None)
    state = models.CharField(max_length=25, default=None)
    city = models.CharField(max_length=100, default=None)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
      

          
