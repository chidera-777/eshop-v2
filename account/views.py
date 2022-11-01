import datetime
from weasyprint import HTML, CSS
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage, BadHeaderError, EmailMultiAlternatives
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from io import BytesIO
from weasyprint import HTML, CSS
from cart.cart import Cart
from .models import Customer,CustomerOrder
from .forms import CustomUserCreationForm, CustomerOrderForm, ConfirmPaymentForm, CustomUserChangeForm, DeleteUserForm

# Create your views here.
def register(request):
    user_form = CustomUserCreationForm()
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            cd = user_form.cleaned_data
            new_user = user_form.save(commit=False)
            new_user.is_active = True
            new_user.save()
            messages.success(request, 'Account created Successfully!')
            subject = f"Welcome to Eshop, {cd['first_name']}"
            html_content = render_to_string('registration/wlcm_email.html')
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [cd['email']])
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            new_user = authenticate(request, email=cd['email'], password=cd['password1'])
            login(request, new_user)
            return redirect('order_register')
    return render(request, 'registration/signup.html', {'user_form':  user_form})
            
def order_register(request):
    cart = Cart(request)
    order_form = CustomerOrderForm()
    if request.method == 'POST':
        order_form = CustomerOrderForm(request.POST)
        if order_form.is_valid():
            cd = order_form.cleaned_data
            user_order = order_form.save(commit=False)
            user_order.user=request.user
            order = user_order.save()
            messages.success(request, 'Info updated Successfully!')
            if cart:
              return redirect('order_payout')
            else:
              return redirect('app:product_list')
    return render(request, 'registration/order.html', {'order_form': order_form})
    
def login_view(request):
    cart = Cart(request)
    if request.method == 'POST':
        valuenext = request.POST.get('next')
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                cart = request.user
                cart.save()
                messages.success(request, 'Login Successful!')
                if valuenext:
                  return redirect(valuenext)
                return redirect('app:product_list')
            else:
                messages.warning(request, 'Your account has been disabled')
                return redirect('login') 
        else:
            messages.error(request, 'User does not exist')
            return redirect('login')
    return render(request, 'registration/login.html', {'cart':cart})
    
def password_reset_view(request):
    password_reset_form = PasswordResetForm()
    if request.method == 'POST':
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            email = password_reset_form.cleaned_data['email']
            try:
              users = get_user_model().objects.get(email=email)
            except get_user_model().DoesNotExist:
              messages.error(request, 'This User is not registered with us ')
              return redirect('password_reset')
            if users is not None:
                subject = "Password Reset Request"
                context = {
                  "email": users.email,
                  "protocol": 'https',
                  "domain": 'eshop-ng.herokuapp.com',
                  'site_name': 'Eshop',
					        "uid": urlsafe_base64_encode(force_bytes(users.pk)),
					        'token': default_token_generator.make_token(users),
                }
                html_content = render_to_string('registration/account/password_reset_email.html', context)
                text_content = strip_tags(html_content)
                msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
                msg.attach_alternative(html_content, 'text/html')
                try:
                  msg.send()
                except BadHeaderError:
                  return HttpResponse('Invalid header found')  
                return redirect('password_reset_done')
    return render(request, "registration/account/password_reset.html", {"password_reset_form":password_reset_form})            
    
def Logout_view(request):
    return render(request, 'registration/logout.html')
    
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out Successfully')
    return redirect('app:product_list')
    
@login_required(login_url='login') 
def user_profile(request):
    try:
      Customer.objects.get(user=request.user)
      return render(request, 'user.html')
    except Customer.DoesNotExist:
      return redirect('order_register')
    
    
@login_required(login_url='login')
def user_edit(request):
    edit_form = CustomUserChangeForm(instance=request.user)
    if request.method == 'POST':
        edit_form = CustomUserChangeForm(instance= request.user, data=request.POST)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, 'Info has been updated')
            return redirect('user_profile')
        else:
            messages.error(request, 'Error updating profile')
    return render(request, 'edit.html', {'edit_form': edit_form})
    
@login_required(login_url='login')
def user_edit_address(request):
    address_form = CustomerOrderForm(instance=request.user.customer)
    if request.method == 'POST':
        address_form = CustomerOrderForm(instance= request.user.customer, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            messages.success(request, 'Info has been updated')
            return redirect('user_profile')
        else:
            messages.error(request, 'Error updating Address')
    return render(request, 'editAddress.html', {'address_form': address_form})

@login_required
def del_user(request):
  if request.method == 'POST':
    email = request.user.email
    del_form = DeleteUserForm(request.POST)
    if del_form.is_valid():
      cd = del_form.cleaned_data
      del_u = authenticate(request, email=email, password=cd['password'])
      if del_u is not None: 
        if del_u.is_active:
          delete_user = get_user_model().objects.get(email=email)
          delete_user.delete()
          messages.success(request, 'User Deleted Successfully!!')
          return redirect('app:product_list')
        else:
          messages.error(request, 'This user is inactive')
          return redirect('app:product_list')
      else:
        messages.error(request, 'Incorrect password')
        return redirect('deleteuser')
  else:
    del_form = DeleteUserForm()
  return render(request, 'delete.html', {'del_form': del_form})    
    
@login_required(login_url='login')
def order_payout(request):
    cart = Cart(request)
    customer = Customer.objects.all()
    try:
      Customer.objects.get(user=request.user)
      return render(request, 'orders/created.html', {'cart': cart, 'customer': customer})
    except Customer.DoesNotExist:
      return redirect('order_register')

@login_required(login_url='login')
def confirm_order(request):
  cart = Cart(request)
  date = datetime.datetime.now().strftime('%d %b %Y')
  order = Customer.objects.get(user=request.user) 
  confirm_form = ConfirmPaymentForm()
  if request.method == 'POST':
    confirm_form = ConfirmPaymentForm(request.POST)
    if confirm_form.is_valid():
        for item in cart:
            customorder = CustomerOrder.objects.create(customer_order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            customorder.save()
        try:
          request.session['coupon_id'] = None
        except:
          pass
        cart.clear()
        order.paid = True
        #payment_completed.delay(custom.id)
        subject = f"Eshop - Invoice no. {order.id}"
        message = "Here are the details of your recent purchase"
        email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [order.user, 'ferdinandchidera49@gmail.com'])
        
        # generate PDF
        html = render_to_string('orders/pdf.html', {'order': order})
        out = BytesIO()
        HTML(string=html).write_pdf(out, stylesheets=[CSS(str(settings.STATIC_ROOT) + '/css/pdf.css')])
        
        # attach PDF
        email.attach('order.pdf', out.getvalue(), 'application/pdf')
        try:
            email.send()
        except BadHeaderError:
          return HttpResponse('Invalid header found')
        messages.success(request, 'Your Order will be processed soon')
        return redirect('app:product_list')
  return render(request, 'orders/confirm.html', {'cart': cart, 'date': date, 'order': order, 'confirm_form': confirm_form})      
        
@staff_member_required
def admin_order_pdf(request, customer_id):
    order = get_object_or_404(Customer, pk=customer_id)
    html = render_to_string('orders/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order.pdf'
    HTML(string=html).write_pdf(response, stylesheets=[CSS(str(settings.STATIC_ROOT) + '/css/pdf.css')])
    return response