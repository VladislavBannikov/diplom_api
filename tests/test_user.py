import json
import unittest
from pprint import pprint

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
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
    user = User.objects.create_user(first_name=data.get('first_name'),
                                    last_name=data.get('last_name'),
                                    email=data.get('email'),
                                    password=data.get('password'),
                                    company=data.get('company'),
                                    position=data.get('position'),
                                    type=data.get('type'),
                                    is_active=True,
                                    )
    print('user create===', user)


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

        # Этот способ не работает. Возвращает True, но заголовка authorization нет в запросе (проверено
        # во вью AccountDetails(APIView) )
        # Из https://www.django-rest-framework.org/api-guide/testing/#authenticating
        # The login method functions exactly as it does with Django's regular Client class. This allows you to authenticate requests against any views which include SessionAuthentication.

        # print('client login===', self.client.login(username="Senya@mail.com", password='123456Qw!'))

        # этот способ работает. Логин, пароль преобразованы в base64
        # self.client.credentials(HTTP_AUTHORIZATION='Basic ' + 'U2VueWFAbWFpbC5jb206MTIzNDU2UXch')

        # Этот способ найден здесь:
        # https://stackoverflow.com/questions/37513050/django-apiclient-login-not-working
        self.client.force_authenticate(User.objects.first())
        print('client.cookies==', self.client.cookies)
        url = reverse('user-details')
        print('client session===', self.client.session)
        response = self.client.get(path=url)
        print('response===', response)
        # print('response.META===')
        print(json.loads(response.content))
