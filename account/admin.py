from django.contrib import admin
from .models import Customer

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['address', 'country', 'state', 'city']
    list_filter = ['created', 'updated']
    search_fields =['user']