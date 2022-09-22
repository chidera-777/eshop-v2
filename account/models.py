from django.db import models
from django.conf import settings 
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from app.models import Product

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, default=None)
    postal_code = models.CharField(max_length=12, default=None)
    country = CountryField(default=None)
    state = models.CharField(max_length=25, default=None)
    city = models.CharField(max_length=100, default=None)
    phone_number = PhoneNumberField(default=None)
    braintree_id = models.CharField(max_length=150, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    