import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from shop.models import User

user_shop_data = {'first_name': 'Pert',
                  'last_name': "Ivanov",
                  'email': "Petr@mail.com",
                  'password': "123456Qw!",
                  'company': "VTB",
                  'position': "manager",
                  'type': "shop"
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


class TestPartner(APITestCase):
    @classmethod
    def setUpClass(cls):
        _create_user(data=user_shop_data)
        super(TestPartner, cls).setUpClass()

    def test_partner_update(self):
        url = reverse('partner-update')
        data = {"url": 'http://127.0.0.1:8000/initdata',
                }
        self.client.force_authenticate(User.objects.get(email='Petr@mail.com'))
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {'Status': True})

#TODO: как лучше организовть запуск тестов? Непонятно как лучше изолировать тесты,
# если они используют единую тестовую базу данных

