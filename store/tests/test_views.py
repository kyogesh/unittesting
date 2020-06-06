from model_mommy import mommy

from django.test import TestCase
from django.test.client import RequestFactory, Client
from django.shortcuts import reverse


class TestIndexView(TestCase):

    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.client = Client()
        self.product = mommy.make('store.Product')

    def test_list_products_view(self):
        resp = self.client.get(reverse('list-products'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.product.name, resp.content.decode('utf-8'))

    def test_product_detail_view(self):
        resp = self.client.get(reverse('show-product', args=[self.product.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.product.name, resp.content.decode('utf-8'))


class TestCartView(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.cart = mommy.make('store.ShoppingCart')
        self.cart_items = mommy.make('store.ShoppingCartItem', _quantity=5, shopping_cart=self.cart)

    def test_one(self):
        resp = self.client.get(reverse('shopping-cart', args=[self.cart.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.cart_items[0].product.name, resp.content.decode('utf-8'))
