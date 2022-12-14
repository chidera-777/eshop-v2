from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from app.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from django.http import JsonResponse
from coupon.forms import CouponForm

# Create your views here.

#@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    add_form = CartAddProductForm(request.POST)
    if add_form.is_valid():
        cd = add_form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
        messages.success(request, '✓ Product added Successfully')
    return redirect('cart:cart_detail')
    
#@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id= product_id)
    cart.remove(product=product)
    messages.success(request, '✓ Product removed from Cart')
    return redirect('cart:cart_detail')
    
def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'override': True})
    coupon_form = CouponForm()
    return render(request, 'cart/detail.html', {'cart': cart, 'coupon_form': coupon_form})
  