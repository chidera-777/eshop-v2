from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.mail import send_mail
from cart.cart import Cart
from .models import Customer
from .forms import CustomUserCreationForm, CustomerOrderForm

# Create your views here.
def register(request):
    user_form = CustomUserCreationForm()
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            cd = user_form.cleaned_data
            new_user = user_form.save()
            messages.success(request, 'Account created Successfully!')
            subject = 'Welcome to Eshop'
            body = f"Dear {cd['first_name']}, \n\n" \
                   f"Thank you for registering with Eshop. \n" \
                   f"We welcome you to enjoy your freedom to shop anywhere, anytime! Sit back and relax while we strive to turn your everyday shopping experience into an extraordinary one."
            try:
                send_mail(subject, body, settings.EMAIL_HOST_USER, [cd['email']], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            new_user = authenticate(request, email=cd['email'], password=cd['password1'])
            login(request, new_user)
            return redirect('order_register')
    return render(request, 'registration/signup.html', {'user_form':  user_form})
            
def order_register(request):
    order_form = CustomerOrderForm()
    if request.method == 'POST':
        order_form = CustomerOrderForm(request.POST)
        if order_form.is_valid():
            cd = order_form.cleaned_data
            user_order = order_form.save(commit=False)
            user_order.user=request.user
            user_order.save()
            messages.success(request, 'Info updated Successfully!')
            return redirect('orders:order_payout')
    return render(request, 'registration/order.html', {'order_form': order_form})
    
def login_view(request):
    cart = Cart(request)
    valuenext = request.POST.get('next')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None and valuenext == '':
            if user.is_active:
                login(request, user)
                cart = request.user
                cart.save()
                messages.success(request, 'Login Successful!')
                return redirect('app:product_list')
            else:
                messages.warning(request, 'Your account has been disabled')
                return redirect('login')
        elif user is not None and valuenext != '':
            if user.is_active:
                login(request, user)
                cart = request.user
                cart.save()
                messages.success(request, 'Login Successful!')
                return redirect(valuenext)
            else:
                messages.warning(request, 'Your account has been disabled')
                return redirect('login')
        else:
            messages.error(request, 'User does not exist')
            return redirect('login')
    return render(request, 'registration/login.html', {'cart':cart})
    
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out Successfully')
    return redirect('login')