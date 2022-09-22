from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.

class CustomUserManagerTest(TestCase):
    
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='example@gmail.com', password='password', first_name='Adam', last_name='Smith')
        self.assertEqual(user.email, 'example@gmail.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.__str__(), user.email)

    def test_super_user(self):
        User = get_user_model()
        superUser = User.objects.create_superuser(email='admin@gmail.com', password='123456789')
        self.assertEqual(superUser.email, 'admin@gmail.com')
        self.assertTrue(superUser.is_active)
        self.assertTrue(superUser.is_staff)
        self.assertTrue(superUser.is_superuser)
        self.assertEqual(superUser.__str__(), superUser.email)
 
        