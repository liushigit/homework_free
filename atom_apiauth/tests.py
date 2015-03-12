from django.test import TestCase

from .views import _generate_key

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

username = 'john'
email = 'abc@abc.com'
password = 'abcde'

def create_user():
    return User.objects.create_user(username, email, password)


class APILoginTest(TestCase):

	def setUp(self):
		create_user()

	def test_login_succeeded(self):
		
		response = self.client.post(reverse('api_login'), 
								   {'username': username,
								   	'password': password
								   })

		
		self.assertEqual(200, response.status_code)
		self.assertEqual('', response.get('API-KEY'))

	def test_login_failed(self):
		response = self.client.post(reverse('api_login'), 
								   {'username': 'someone',
								   	'password': password
								   })

		
		self.assertEqual(400, response.status_code)



class SimpleTest(TestCase):
    def test_gen_key(self):
        key = _generate_key()
        self.assertEqual('', key)
