from django.contrib import admin
from .models import Category, Product, Newsletter

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  list_display = ['name', 'slug', 'image']
  prepopulated_fields = {'slug': ('name',)}
  
@admin.register(Product)  
class ProductAdmin(admin.ModelAdmin):
  list_display = ['name', 'slug', 'available', 'deals', 'price', 'created', 'updated']
  list_filter = ['available', 'created', 'updated']
  list_editable = ['price', 'available']
  prepopulated_fields = {'slug': ('name',)}
  
@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display=['email']