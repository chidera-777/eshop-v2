import braintree
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from account.models import Customer
from cart.cart import Cart
from django.contrib.auth.decorators import login_required

# Create your views here.
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)

@login_required(login_url='login')
def payment_process(request):
    cart = Cart(request)
    customer_id =request.session.get('customer_id')
    order = get_object_or_404(Customer, id=customer_id)
    total_price = cart.get_total_price()
    if request.method == "POST":
        nonce =request.POST.get('payment_method_nonce', None)
        result = gateway.transaction.sale({
          'amount':f'{total_price:.2f}',
          'payment_method_nonce': nonce,
          'options':{
            'submit_for_settlement': True
          }
        })
        if result.is_success:
            # clear the cart
            cart.clear()
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('payment:done'
        else:
          return redirect('payment:cancelled')
    else:
        client_token = gateway.client_token.generate()
        return render(request,'process.html', {'cart': cart, 'order': order, 'client_token': client_token})

@login_required(login_url='login')          
def payment_done(request):
    return render(request, 'done.html')

@login_required(login_url='login')    
def payment_cancelled(request):
    return render(request, 'cancelled.html')