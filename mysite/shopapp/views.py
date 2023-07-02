from django.http import HttpRequest
from django.shortcuts import render


def shop_index(request: HttpRequest):
    products = [
        ('Laptop', 1999),
        ('Desktop', 2999),
        ('Smartphone', 999),
    ]
    context = {
        "products": products,
    }
    return render(request, 'shopapp/shop-index.html', context=context)
