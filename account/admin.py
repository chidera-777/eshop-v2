from django.contrib import admin
from django import forms
from .models import Customer


# Register your models here.

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['address', 'country', 'state', 'phone_number', 'city']
    list_filter = ['created', 'updated']
    search_fields = ['user']
