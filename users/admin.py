from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

# Register your models here.
class CustomUserAdmin(UserAdmin):
    fieldsets = (
      (None, {'fields': ('email', 'password')}), 
      (('Personal info'), {'fields': ('first_name', 'last_name')}),
      (('Permissions'), {'fields': ('is_staff', 'is_active')}), 
    )
    add_fieldsets =(
      (None, {
        'classes': ('wide',), 
        'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')}
      ),
    )
    list_display = ['email', 'first_name', 'last_name', 'is_staff']
    list_filter = ['email', 'is_staff', 'is_active']
    search_fields = ['first_name', 'last_name']
    ordering = ('email',)  

admin.site.register(get_user_model(), CustomUserAdmin)