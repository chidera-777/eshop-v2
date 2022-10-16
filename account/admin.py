from django.contrib import admin
from .models import Customer, CustomerOrder
from django.urls import reverse
from django.utils.safestring import mark_safe

# Register your models here.

def order_pdf(obj):
   url = reverse('admin_order_pdf', args=[obj.id])
   return mark_safe(f'<a href="{url}">PDF</a>')
order_pdf.short_description = 'Invoice'

class CustomerOrderInline(admin.TabularInline):
    model = CustomerOrder
    raw_id_fields = ['product']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'country', 'state', 'phone_number', 'city', order_pdf]
    list_filter = ['created', 'updated']
    inlines = [CustomerOrderInline]
    search_fields = ['user__email']
