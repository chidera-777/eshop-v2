from django.urls import path
from .import views

app_name = 'app'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('search/', views.search_list, name='search_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_category'),
    path('<int:id>/<slug:slug>/', views.product_details, name='product_details'),
  ]