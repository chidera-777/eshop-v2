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
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    
    def __str__(self):
      return f'{self.user}'
      
    def get_total_cost(self):
      total_cost = sum(item.get_cost() for item in self.items.all())
      return total_cost
    
class CustomerOrder(models.Model):
    customer_order = models.ForeignKey(Customer, related_name='items', on_delete=models.CASCADE, default=None)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, default=None)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=None)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
      return str(self.id)
      
    def get_cost(self):
      return self.price * self.quantity