import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from shop_user.models import User

TEST_USER = "Shop1@mail.com"


class TestOrderShop(APITestCase):
    fixtures = ['user.json', 'shop_product_productinfo_productparameter.json', 'order_orderitem__order_buyer.json',
                'contact.json']

    def test_order_shop_list(self):
        url = reverse('shop:partner-orders')
        self.client.force_authenticate(User.objects.get(email=TEST_USER))
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
