import json
import unittest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from shop.models import User

user_data = {'first_name': 'Senya',
             'last_name': "Ivanov",
             'email': "Senya@mail.com",
             'password': "123456Qw!",
             'company': "VTB",
             'position': "manager",
             'type': "buyer"
             }

def _create_user(data):
    User.objects.create(first_name=data.get('first_name'),
                        last_name=data.get('last_name'),
                        email=data.get('email'),
                        password=data.get('password'),
                        company=data.get('company'),
                        position=data.get('position'),
                        type=data.get('type'),
                        is_active=True)

@unittest.skip
class TestRegisterAccount(APITestCase):

    def test_create_user(self):
        url = reverse('user-register')
        response = self.client.post(path=url, data=user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {'Status': True})
        self.assertEqual(User.objects.all().count(), 1)


class TestLogin(APITestCase):

    @classmethod
    def setUpClass(cls):
        _create_user(data=user_data)
        super(TestLogin, cls).setUpClass()

    def test_login_account(self):
        print(User.objects.all())

        client = APIClient()
        print(client.login(user="Senya@mail.com", password='123456Qw!'))


