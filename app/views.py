from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.db.models import Q

# Create your views here.
def product_list(request, category_slug=None):
  category = None
  categories = Category.objects.all()  
  products = Product.objects.filter(available=True)
  if category_slug:
    category = get_object_or_404(Category, slug=category_slug)
    products = products.filter(category=category)
  return render(request, 'products/list.html', {'category': category, 'categories': categories, 'products': products})
  
def product_details(request, id, slug):
   product = get_object_or_404(Product, id=id, slug=slug, available=True)
   cart_product_form = CartAddProductForm()
   return render(request, 'products/detail.html',  {'product': product, 'cart_product_form': cart_product_form})

def search_list(request):
    search_query = Product.objects.filter(Q(category__name__icontains=request.GET['q']) | Q(name__icontains=request.GET['q'])
    )
    return render(request, 'product/search.html', { 'search_query': search_query})