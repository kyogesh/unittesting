from django.shortcuts import render
from django.views import generic
from store.models import Product, ShoppingCart


class IndexView(generic.ListView):
    template_name = 'store/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all()


class ProductDetailView(generic.DetailView):
    template_name = 'store/product.html'
    context_object_name = 'product'
    model = Product


class CartView(generic.DetailView):
    template_name = 'store/cart.html'
    context_object_name = 'cart'
    model = ShoppingCart
