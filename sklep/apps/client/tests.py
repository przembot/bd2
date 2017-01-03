from django.test import TestCase, Client
import apps.client.views as views
from apps.accounts.models import CustomUser
from apps.accounts.models import Client as CustomClient
from django.shortcuts import reverse
from django.http import HttpResponse, HttpResponseBadRequest

class ClientViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser',
                                                   password='test',
                                                   birthdate='2000-01-01')
        self.customclient = CustomClient.objects.create(user = self.user)

    def test_make_order_not_logged_in(self):
        self.assertEqual(self.client.post(reverse('order')).status_code, 302)

    def test_make_order_get_method(self):
        self.assertTrue(self.client.login(username='testuser', password='test'))
        response = self.client.get(reverse('order'), follow=True)
        self.assertEqual(response.status_code, HttpResponse().status_code)

    def test_make_order_empty_body(self):
        self.assertTrue(self.client.login(username='testuser', password='test'))
        self.assertRaises(Exception, self.client.post, reverse('order'), follow=True)

    def test_make_order_correct(self):
        pass 
