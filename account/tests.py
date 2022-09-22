from django.test import TestCase
from .models import Customer
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.http import HttpRequest

# Create your tests here.

class CreateAccountTest(TestCase):

    def test_signup_page_status_code(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)
        
    def test_signup_url_by_name_and_uses_correct_template(self):
        response = self.client.get(reverse ('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')
        
    def test_signup_empty_form(self):
        form = CustomUserCreationForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('password1', form.fields)
        self.assertIn('password2', form.fields)
        
    def test_signup_post_form(self):
        request = HttpRequest()
        request.POST = {
          'email': "example@gmail.com",
          'first_name': 'Adam',
          'last_name': 'Smith',
          'password1': 'qazxswedcvfr',
          'password2': 'qazxswedcvfr',
        }
        form = CustomUserCreationForm(request.POST)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(get_user_model().objects.all().count(), 1)
        
        
        
        
    #def test_clean_password2(self):
        #user = CustomUserCreationForm(data={"email":'example@gmail.com', 'first_name':'Adam', 'last_name':'Smith', 'password1':'password', 'password2':'password'})
        #clean = user.clean_password
        #cd=clean(self)
        #self.assertEqual(cd('password1'), cd('password2'))
        
    