from django.contrib import admin
from .models import OrderItem

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    