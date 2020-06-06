"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from store import views, api_views

urlpatterns = [
    path('api/v1/products/', api_views.ProductList.as_view(), name='product-list-api'),
    path('api/v1/products/new', api_views.ProductCreate.as_view(), name='product-create-api'),
    path('api/v1/products/<int:id>/', api_views.ProductRetrieveUpdateDestroy.as_view(), name='product-rud'),
    # path('api/v1/products/<int:id>/destroy', api_views.ProductDestroy.as_view(), name='product-delete-api'),

    path('admin/', admin.site.urls),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='show-product'),
    path('cart/<int:pk>/', views.CartView.as_view(), name='shopping-cart'),
    path('', views.IndexView.as_view(), name='list-products'),
]
