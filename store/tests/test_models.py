import datetime

from model_mommy import mommy
from django.test import TestCase
from django.utils import timezone
from store.models import Product, ShoppingCart, ShoppingCartItem


class TestProduct(TestCase):

    def test_can_create_product(self) -> None:
        mommy.make('store.Product')
        self.assertEqual(Product.objects.count(), 1)

    def test_product_on_sale(self) -> None:
        sale_start = timezone.now()
        sale_end = timezone.now() + datetime.timedelta(days=1)
        product = mommy.make('store.Product', sale_start=sale_start, sale_end=sale_end)
        self.assertTrue(product.is_on_sale())
        self.assertTrue(product.is_on_sale())

    def test_product_not_on_sale(self):
        product = mommy.make('store.Product')
        self.assertFalse(product.is_on_sale())

    def test_product_sale_ended(self):
        sale_start = timezone.now() - datetime.timedelta(days=1)
        sale_end = timezone.now() - datetime.timedelta(minutes=10)
        product = mommy.make('store.Product', sale_start=sale_start, sale_end=sale_end)
        self.assertFalse(product.is_on_sale())

    def test_sale_end_not_set(self):
        product = mommy.make('store.Product', sale_start=timezone.now(), sale_end=None)
        self.assertTrue(product.is_on_sale())

    def test_rounded_off_price_to_two_decimal_points(self):
        product = mommy.make('store.Product', price=99.9777777)
        self.assertEqual(product.get_rounded_price(), 99.98)

    def test_current_price_for_product_on_sale(self):
        product = mommy.make('store.Product', sale_start=timezone.now())
        price = product.price
        self.assertEqual(product.current_price(), round(price * (1 - product.DISCOUNT_RATE), 2))

    def test_current_price_for_product_not_on_sale(self):
        product = mommy.make('store.Product')
        price = product.price
        self.assertEqual(product.current_price(), round(price, 2))

    def test_model_string_representation(self):
        product = mommy.make('store.Product')
        expected_value = '<Product object ({product.id}) "{product.name}">'.format(product=product)
        self.assertEqual(expected_value, repr(product))


class TestShoppingCart(TestCase):

    def test_create_shopping_cart(self):
        cart = mommy.make('store.ShoppingCart')
        self.assertEqual(ShoppingCart.objects.count(), 1)

    def test_amount_of_empty_cart(self):
        cart = mommy.make('store.ShoppingCart')
        self.assertEqual(cart.total(), 0.0)

    def test_model_string_representation(self):
        cart = mommy.make('store.ShoppingCart')
        expected_value = '<ShoppingCart object ({cart.id}) "{cart.name}" "{cart.address}">'.format(cart=cart)
        self.assertEqual(expected_value, repr(cart))


class TestShoppingCartItem(TestCase):

    def test_create_shopping_cart_item(self):
        mommy.make(ShoppingCartItem)
        self.assertEqual(ShoppingCartItem.objects.count(), 1)

    def test_check_shopping_cart_item_total(self):
        cart_item = mommy.make(ShoppingCartItem, quantity=10, product__price=9)
        self.assertEqual(cart_item.total(), 90)

    def test_create_shopping_cart_total(self):
        cart_item = mommy.make('store.ShoppingCartItem', quantity=1, product__price=10.0)
        self.assertEqual(cart_item.shopping_cart.total(), 11.30)

    def test_shopping_cart_with_different_items_cart_value(self):
        cart = mommy.make(ShoppingCart)
        mommy.make(ShoppingCartItem, quantity=9, shopping_cart=cart, product__price=6.50)
        mommy.make(ShoppingCartItem, quantity=2, shopping_cart=cart, product__price=50.0)
        mommy.make(ShoppingCartItem, quantity=1, shopping_cart=cart, product__price=17.80)
        mommy.make(ShoppingCartItem, quantity=4, shopping_cart=cart, product__price=37.25)
        self.assertEqual(cart.total(), 367.59)

    def test_model_string_representation(self):
        cart_item = mommy.make('store.ShoppingCartItem')
        expected_value = '<ShoppingCartItem object ({cart_item.id}) ' \
                         '{cart_item.quantity}x "{cart_item.product.name}">'.format(cart_item=cart_item)
        self.assertEqual(expected_value, repr(cart_item))
