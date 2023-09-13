from django.contrib.auth.models import User
from django.core.cache import cache
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]
    search_fields = ["name", "description"]
    ordering_fields = [
        "pk",
        "name",
        "price",
        "discount",
    ]


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]
    filterset_fields = [
        "user",
        "products",
        "delivery_adress",
        "promocode",
    ]
    ordering_fields = [
        "pk",
        "user",
        "products",
        "delivery_adress",
        "promocode",
    ]


class UserOrdersExportView(APIView):
    @staticmethod
    def get(request: HttpRequest, user_id) -> JsonResponse:
        cache_key = f'user_{user_id}_orders'
        cached_data = cache.get(cache_key)
        if cached_data:
            return JsonResponse(cached_data, safe=False)

        user = get_object_or_404(User, id=user_id)
        orders = Order.objects.filter(user=user).order_by("pk")
        data = OrderSerializer(orders, many=True).data

        cache.set(cache_key, data, 300)
        return JsonResponse(data, safe=False)
