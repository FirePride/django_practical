from django.http import HttpRequest
from django.shortcuts import render

from .models import Product, Order


def shop_index(request: HttpRequest):
    menu = [
        ('products', 'Products in the shop'),
        ('orders', 'Orders in the shop'),
    ]
    context = {
        "menu": menu,
    }
    return render(request, 'shopapp/shop-index.html', context=context)


def products_list(request: HttpRequest):
    context = {
        "products": Product.objects.all(),
    }
    return render(request, 'shopapp/products-list.html', context=context)


def orders_list(request: HttpRequest):
    context = {
        "orders": Order.objects.select_related("user").prefetch_related("products").all(),
    }
    return render(request, 'shopapp/orders-list.html', context=context)
