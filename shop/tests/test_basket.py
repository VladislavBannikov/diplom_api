from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from shop_user.models import User

TEST_USER = "Dima@mail.com"
TEST_ORDER_ITEM_ID = 12


class TestBasket(APITestCase):
    fixtures = ['user.json', 'shop_product_productinfo_productparameter.json', 'order_orderitem.json']

    def test_basket_list(self):
        url = reverse('shop:basket-list-apiview')
        self.client.force_authenticate(User.objects.get(email=TEST_USER))
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_basket_add(self):
        url = reverse('shop:basket-list')
        data = {
            "quantity": 1,
            "product_info": 1
        }
        self.client.force_authenticate(User.objects.get(email=TEST_USER))
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_basket_delete(self):
        url = reverse('shop:basket-detail', args=[TEST_ORDER_ITEM_ID])
        self.client.force_authenticate(User.objects.get(email=TEST_USER))
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_basket_add(self):
        url = reverse('shop:basket-detail', args=[TEST_ORDER_ITEM_ID])
        data = {
            "quantity": 111,
        }
        self.client.force_authenticate(User.objects.get(email=TEST_USER))
        response = self.client.patch(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
