from django.test import TestCase, Client, RequestFactory
import apps.client.views as views
from apps.accounts.models import CustomUser, Client as CustomClient
from django.shortcuts import reverse
from django.http import HttpResponse, HttpResponseBadRequest
from apps.dao.models import Item
import json

class ClientViewTestCase(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser',
                                                   password='test',
                                                   birthdate='2000-01-01')
        self.customclient = CustomClient.objects.create(user = self.user)
        self.factory = RequestFactory()

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
        item11Before = Item.objects.get(id=11)
        item12Before = Item.objects.get(id=12)
        item11InOrderAmount = 3
        item12InOrderAmount = 2
        philipsSpec = {'id' : item11Before.id, 'amount' : item11InOrderAmount}
        boschSpec   = {'id' : item12Before.id,   'amount' : item12InOrderAmount}
        order = {'items' : (philipsSpec, boschSpec), 'invoice' : False}

        self.assertTrue(self.client.login(username='testuser', password='test'))

        request = self.factory.post(reverse('order'),
                                    data=json.dumps(order, ensure_ascii=False),
                                    content_type='application/json')
        request.user = self.user
        response = views.make_order(request)

        self.assertEqual(response.status_code, HttpResponse().status_code)
        self.assertEqual(Item.objects.get(name=item11Before.name).in_stock,
                         item11Before.in_stock - item11InOrderAmount)
        self.assertEqual(Item.objects.get(name=item12Before.name).in_stock,
                         item12Before.in_stock - item12InOrderAmount)

    def test_make_order_incorrect_amount(self):
        item11Before = Item.objects.get(id=11)
        item12Before = Item.objects.get(id=12)
        item11InOrderAmount = item11Before.in_stock + 2
        item12InOrderAmount = 2
        item11Spec = {'id' : item11Before.id, 'amount' : item11InOrderAmount}
        item12Spec = {'id' : item12Before.id,   'amount' : item12InOrderAmount}
        order = {'items' : [item11Spec, item12Spec], 'invoice' : False}

        self.assertTrue(self.client.login(username='testuser', password='test'))

        request = self.factory.post(reverse('order'),
                                    data=json.dumps(order, ensure_ascii=False),
                                    content_type='application/json')
        request.user = self.user
        response = views.make_order(request)

        self.assertEqual(response.status_code, HttpResponseBadRequest().status_code)
        self.assertEqual(Item.objects.get(name=item11Before.name).in_stock,
                         item11Before.in_stock)
        self.assertEqual(Item.objects.get(name=item12Before.name).in_stock,
                         item12Before.in_stock)

    def test_make_order_not_existing_item(self):
        imaginaryItemId = 3
        imaginaryItemAmount = 5
        imaginaryItemSpec = {'id' : imaginaryItemId, 'amount' : imaginaryItemAmount}
        order = {'items' : [imaginaryItemSpec], 'invoice' : False}

        self.assertTrue(self.client.login(username='testuser', password='test'))

        request = self.factory.post(reverse('order'),
                                    data=json.dumps(order, ensure_ascii=False),
                                    content_type='application/json')
        request.user = self.user
        response = views.make_order(request)

        self.assertEqual(response.status_code, HttpResponseBadRequest().status_code)
