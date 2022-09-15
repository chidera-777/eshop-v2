from django.db import models
from app.models import Product

# Create your models here.

class OrderItem(models.Model):
    #order = models.ForeignKey(Order, related_name='items', on_delete= models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    paid = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.id}'
        
    def get_cost(self):
        return self.price * self.quantity
