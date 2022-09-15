from django import forms
from .models import OrderItem

class OrderCreateForm(forms.ModelForm):
    model = OrderItem
    fields = ['price', 'quantity']