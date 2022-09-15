from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

#app_name = 'account'

urlpatterns = [
    path('signup/', views.register, name='register'),
    path('signup/order/', views.order_register, name='order_register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
       ## Password Change urls ##
    path('passwordChange/', auth_views.PasswordChangeView.as_view(template_name='registration/account/password_change.html'), name='password_change'),
    path('passwordChangeDone/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/account/password_change_done.html'), name='passwordChangeDone'),
   
     ## password reset urls ##
    path('passwordReset/', auth_views.PasswordResetView.as_view(template_name='registration/account/password_reset.html'), name='password_reset'),
     path('passwordReset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/account/password_reset_done.html'), name='password_reset_done'),
     path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/account/password_reset_confirm.html'), name='password_reset_confirm'),
     path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/account/password_reset_complete.html'), name='password_reset_complete'),
  ]