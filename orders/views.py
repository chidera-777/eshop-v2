from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from account.models import Customer

# Create your views here.
@login_required(login_url='login')
def order_payout(request):
    cart = Cart(request)
    customer = Customer.objects.all()
    return render(request, 'orders/created.html', {'cart': cart, 'customer': customer})


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            #clear cart
            cart.clear()
            return render(request, 'orders/created.html', {'order': order})
    else:
      form = OrderCreateForm()
    return render(request, 'orders/create.html', {'cart': cart, 'form': form})