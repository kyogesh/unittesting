import json
import datetime

from model_mommy import mommy

from django.core.files.uploadedfile import UploadedFile
from django.shortcuts import reverse
from django.test.client import Client
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient, APITestCase

from store.models import Product


class TestProductList(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.products = mommy.make('store.Product', _quantity=4, sale_start=None, sale_end=None)
        sale_start = timezone.now() - datetime.timedelta(days=1)
        sale_end = timezone.now() + datetime.timedelta(days=1)
        self.products_on_sale = mommy.make('store.Product', sale_start=sale_start, sale_end=sale_end, _quantity=3)

    def test_get_all_products(self):
        resp = self.client.get(reverse('product-list-api'))
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content.decode('utf-8'))
        self.assertEqual(len(content['results']), 7)

    def test_get_products_on_sale_true(self):
        resp = self.client.get(reverse('product-list-api'), dict(on_sale=True))
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content.decode('utf-8'))
        self.assertEqual(len(content['results']), 3)

    def test_get_products_on_sale_false(self):
        resp = self.client.get(reverse('product-list-api'), dict(on_sale=False))
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content.decode('utf-8'))
        self.assertEqual(len(content['results']), 7)

    def test_pagination(self):
        mommy.make('store.Product', _quantity=5)
        resp = self.client.get(reverse('product-list-api'))
        content = json.loads(resp.content.decode('utf-8'))
        self.assertEqual(content['count'], 12)
        self.assertEqual(len(content['results']), 10)


class TestProductCreate(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_can_create_product(self):
        request_data = {'name': 'Product X', 'description': 'Latest model Product X', 'price': 97.99}
        resp = self.client.post(reverse('product-create-api'), data=request_data)
        self.assertEqual(resp.status_code, 201)
        content = json.loads(resp.content.decode('utf-8'))
        self.assertEqual(content['name'], request_data['name'])

    def test_try_create_product_with_invalid_price(self):
        request_data = {'name': 'Product X', 'description': 'Latest model Product X', 'price': 'None'}
        resp = self.client.post(reverse('product-create-api'), data=request_data)
        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content.decode('utf-8'))
        self.assertIn('price', content)
        self.assertEqual(content['price'], 'A valid number is required')

    def test_try_create_product_with_price_zero(self):
        request_data = {'name': 'Product X', 'description': 'Latest model Product X', 'price': '0.0'}
        resp = self.client.post(reverse('product-create-api'), data=request_data)
        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content.decode('utf-8'))
        self.assertIn('price', content)
        self.assertEqual(content['price'], 'Must be above $0.00')


class TestProductRetrieveUpdateDestroy(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.products = mommy.make('store.Product', _quantity=2)

    def test_retrieve_product(self):
        resp = self.client.get(reverse('product-rud', args=[self.products[0].pk, ]))
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertEqual(content['name'], self.products[0].name)

    def test_update_product(self):
        data = {'price': 99.59, 'name': 'New Product', 'description': 'New description for product'}
        resp = self.client.put(reverse('product-rud', args=[self.products[1].pk, ]), data=data)
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content.decode('utf-8'))
        self.assertEqual(float(content['price']), data['price'])
        self.assertEqual(content['name'], data['name'])

    def test_delete_product(self):
        resp = self.client.delete(reverse('product-rud', args=[self.products[0].pk, ]))
        self.assertEqual(resp.status_code, 204)

    def test_update_product_warranty(self):
        data = {'price': 59.59, 'name': 'New Product One', 'description': 'New description for One',
                'warranty': open('warranty.txt')}
        resp = self.client.put(reverse('product-rud', args=[self.products[1].pk, ]), data=data)
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content.decode('utf-8'))
        self.assertIn('Warranty Information:', content['description'])
