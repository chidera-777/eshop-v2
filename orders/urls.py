from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_payout, name='order_payout'),
    
  ]