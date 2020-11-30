import json
import unittest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from shop_user.models import User, Contact

TEST_EMAIL = "Shop1@mail.com"
TEST_PASSWORD = "123456Qw!"

SHOP_CONTACT_ID = 7
BUYER_CONTACT_ID = 2


class TestContact(APITestCase):
    fixtures = ['user.json', 'contact.json']

    def test_contact_create(self):
        data = {
            "city": "Moscow",
            "street": "Solyanka1",
            "phone": "+7000002"
        }
        self.client.force_authenticate(User.objects.get(email=TEST_EMAIL))
        url = reverse('user:contact-list')
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_contact_list(self):
        self.client.force_authenticate(User.objects.get(email=TEST_EMAIL))
        url = reverse('user:contact-list')
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        contact_ids_db = [c.id for c in Contact.objects.filter(user__email=TEST_EMAIL)]
        contact_ids_query = [c['id'] for c in json.loads(response.content)]
        self.assertListEqual(contact_ids_db, contact_ids_query)

    def test_contact_delete(self):
        self.client.force_authenticate(User.objects.get(email=TEST_EMAIL))
        url = reverse('user:contact-detail', args=[SHOP_CONTACT_ID])
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # negative test, contact can't be deleted under the shop user.
        url = reverse('user:contact-detail', args=[BUYER_CONTACT_ID])
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_contact_edit(self):
        test_city_name = "Moscow_test"
        data = {
            "city": test_city_name,
        }
        self.client.force_authenticate(User.objects.get(email=TEST_EMAIL))
        url = reverse('user:contact-detail', args=[SHOP_CONTACT_ID])
        response = self.client.patch(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
