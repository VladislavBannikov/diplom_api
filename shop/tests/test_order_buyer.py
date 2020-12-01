import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from shop_user.models import User

TEST_USER = "Dima@mail.com"
TEST_ORDER_ITEM_ID = 12


class TestOrderBuyer(APITestCase):
    fixtures = ['user.json', 'shop_product_productinfo_productparameter.json', 'order_orderitem__order_buyer.json',
                'contact.json']

    def test_order_buyer_list(self):
        url = reverse('shop:orderbuyer-list')
        self.client.force_authenticate(User.objects.get(email=TEST_USER))
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_buyer_create(self):
        url = reverse('shop:orderbuyer-list')
        data = {
            "contact_id": 2,
        }
        self.client.force_authenticate(User.objects.get(email=TEST_USER))
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
