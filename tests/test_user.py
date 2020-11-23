import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from shop.models import User


class TestAccountCreateUser(APITestCase):
    user_data_local = {'first_name': 'Senya_local',
                       'last_name': "Ivanov",
                       'email': "Senya_local@mail.com",
                       'password': "123456Qw!",
                       'company': "VTB",
                       'position': "manager",
                       'type': "buyer"
                       }

    def test_create_user(self):
        url = reverse('user-list')
        response = self.client.post(path=url, data=self.user_data_local)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestAccount(APITestCase):
    fixtures = ['shop_dump.json', ]

    def test_account_detail(self):
        # Этот способ не работает. Возвращает True, но заголовка authorization нет в запросе (проверено
        # во вью AccountDetails(APIView) )
        # Из https://www.django-rest-framework.org/api-guide/testing/#authenticating
        # The login method functions exactly as it does with Django's regular Client class. This allows you to authenticate requests against any views which include SessionAuthentication.

        # print('client login===', self.client.login(username="Senya@mail.com", password='123456Qw!'))

        # этот способ работает. Логин, пароль преобразованы в base64
        # self.client.credentials(HTTP_AUTHORIZATION='Basic ' + 'U2VueWFAbWFpbC5jb206MTIzNDU2UXch')

        # Этот способ найден здесь:
        # https://stackoverflow.com/questions/37513050/django-apiclient-login-not-working
        self.client.force_authenticate(User.objects.get(email='Dima@mail.com'))
        url = reverse('user-detail')
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_token(self):
        url = reverse('api_token_auth')
        data = {"username": "Dima@mail.com",
                "password": "123456Qw!"
                }
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", json.loads(response.content))

    def test_account_edit(self):
        data = {"first_name": "test_name"}
        self.client.force_authenticate(User.objects.get(email='Dima@mail.com'))
        url = reverse('user-edit')
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(email='Dima@mail.com').first_name, data.get("first_name"))
