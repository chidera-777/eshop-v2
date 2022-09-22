from django.test import TestCase, Client
from django.utils import timezone
from .models import Category, Product
from django.urls import reverse

# Create your tests here.

 ## For models ##
client = Client()
class CategoryTest(TestCase):
  
    def create_category(self, name='name', slug='slug'):
        return Category.objects.create(name=name, slug=slug)
        
    def test_created_category(self):
        category = self.create_category()
        url = reverse('app:product_list_category', args=[category.slug])
        resp = self.client.get(url)
        self.assertTrue(isinstance(category, Category))
        self.assertEqual(category.__str__(), category.name)
        self.assertEqual(resp.status_code, 200)
        #self.assertIn(category.slug, resp.content)
        
class ProductTest(TestCase):
    
    def create_product(self, name='name', slug='slug', price=000):
        category = Category.objects.create(name=name, slug=slug)
        return Product.objects.create(category=category, name=name, slug=slug, price=price, created=timezone.now())
    
    def test_created_product(self):
        product = self.create_product()
        url = reverse('app:product_details', args=[product.id, product.slug])
        resp = self.client.get(url)
        self.assertTrue(isinstance(product, Product))
        self.assertEqual(product.__str__(), product.name)
        self.assertEqual(resp.status_code, 200)
        
