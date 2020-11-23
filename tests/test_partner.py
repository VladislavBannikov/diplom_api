import json
import unittest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from shop.models import User


@unittest.skip
# TODO: fix this
class TestPartner(APITestCase):
    fixtures = ['user_token_etc.json', ]

    def test_partner_update(self):
        url = reverse('partner-update')
        data = {"url": 'http://127.0.0.1:8000/initdata',
                }
        self.client.force_authenticate(User.objects.get(email='DNS@mail.com'))
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {'Status': True})


#TODO: как лучше организовть запуск тестов? Непонятно как лучше изолировать тесты,
# если они используют единую тестовую базу данных

