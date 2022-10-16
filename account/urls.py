from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

#app_name = 'account'

urlpatterns = [
    path('signup/', views.register, name='register'),
    path('signup/order/', views.order_register, name='order_register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.Logout_view, name='Logout'),
    path('Logout/', views.logout_view, name='logout'),
    path('profile/', views.user_profile, name='user_profile'),
    path('edit/', views.user_edit, name='user_edit'),
    path('edit/address/', views.user_edit_address, name='user_edit_address'),
    path('delete/', views.del_user, name='deleteuser'),
    
       ## Password Change urls ##
    path('passwordChange/', auth_views.PasswordChangeView.as_view(template_name='registration/account/password_change.html'), name='password_change'),
    path('passwordChangeDone/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/account/password_change_done.html'), name='passwordChangeDone'),
   
     ## password reset urls ##
    path('passwordReset/', views.password_reset_view, name='password_reset'),
     path('passwordReset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/account/password_reset_done.html'), name='password_reset_done'),
     path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/account/password_reset_confirm.html'), name='password_reset_confirm'),
     path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/account/password_reset_complete.html'), name='password_reset_complete'),
     path('', views.order_payout, name='order_payout'),
     path('admin/order/<int:customer_id>/pdf', views.admin_order_pdf, name='admin_order_pdf'),
     path('confirm/', views.confirm_order, name='confirm_order'),
  ]