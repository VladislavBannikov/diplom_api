import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from shop.models import User


TEST_USER = "Shop1@mail.com"
TEST_PASSWORD = "123456Qw!"
INIT_DATA_URL = f'http://localhost:8000{reverse("shop:init-data")}'


# This test requires test server to be run
class TestPartner(APITestCase):
    fixtures = ['user.json', ]

    def test_partner_update(self):
        url = reverse('shop:partner-update')
        data = {"url": INIT_DATA_URL,
                }
        self.client.force_authenticate(User.objects.get(email=TEST_USER))
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {'Status': True})
