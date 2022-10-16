from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
  name = models.CharField(max_length=200, db_index=True)
  slug = models.SlugField(max_length=200, unique=True)
  image = models.ImageField(upload_to='category/%Y/%m/%d', blank=True)
  
  class Meta:
    ordering = ('name',)
    verbose_name = 'category'
    verbose_name_plural = 'categories'
  
  def __str__(self):
    return self.name
    
  def get_absolute_url(self):
    return reverse('app:product_list_category', args=[self.slug])
    

class Product(models.Model):
  category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
  name = models.CharField(max_length=200, db_index=True)
  slug = models.SlugField(max_length=200, db_index=True)
  image = models.ImageField(upload_to='product/%Y/%m/%d', blank=True)
  description = models.TextField(blank=True)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  available = models.BooleanField(default=True)
  deals = models.BooleanField(default=False)
  old_price = models.DecimalField(blank=True, default=None, null=True, max_digits=10, decimal_places=2)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  
  class Meta:
    ordering = ('name',)
    index_together = (('id', 'slug'),)
    
  def __str__(self):
    return self.name
    
  def get_absolute_url(self):
      return reverse('app:product_details', args=[self.id, self.slug])
      
class Newsletter(models.Model):
  email = models.EmailField(unique=True)
  
  def __str__(self):
    return self.email