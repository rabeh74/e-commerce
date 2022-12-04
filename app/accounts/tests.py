from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
# Create your tests here.
class TestUser(TestCase):
    def setUp(self):
        self.client=Client()

    def test_create_user(self):
        user=get_user_model().objects.create_user(
            user_name='rabeh'
            ,email='bohaa@email.com',
            password='test123%6#',
            first_name='rabeh2',
            last_name='rabie',
            )
        self.assertEqual(user.email, 'bohaa@email.com')
        self.assertEqual(user.user_name, 'rabeh')

        self.assertTrue(user.check_password('test123%6#'))


