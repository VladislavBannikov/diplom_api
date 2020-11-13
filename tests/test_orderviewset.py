import unittest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
# from myproject.apps.core.models import Account
# from diplom_api import settings
from shop.models import User


@unittest.skip
class TestOrderViewSet(APITestCase):
    def test_order_listing(self):
        url = reverse('order-list')
        print("TestOrderViewSet-----", User.objects.all())

        print(self.client.login(username='Senya@mail.com', password='123456Qw!'))
        # self.client.lo
        response = self.client.get(url)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(response.status_code)
        print(self.client)



# class AccountTests(APITestCase):
#     def test_create_account(self):
#         """
#         Ensure we can create a new account object.
#         """
#         url = reverse('account-list')
#         data = {'name': 'DabApps'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Account.objects.count(), 1)
#         self.assertEqual(Account.objects.get().name, 'DabApps')


if __name__ == '__main__':
    unittest.main()

