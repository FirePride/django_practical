from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    shop_index,
    ProductDetailView,
    ProductListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    OrdersListView,
    OrderDetailView,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,
    OrdersExportView,
    ProductViewSet,
    OrderViewSet,
)

app_name = "shopapp"

routers = DefaultRouter()
routers.register("products", ProductViewSet)
routers.register("orders", OrderViewSet)

urlpatterns = [
    path("", shop_index, name="index"),
    path("api/", include(routers.urls)),
    path("products/", ProductListView.as_view(), name="products_list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="products_details"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/update/<int:pk>/", ProductUpdateView.as_view(), name="product_update"),
    path("products/archive/<int:pk>/", ProductDeleteView.as_view(), name="product_archive"),
    path("orders/", OrdersListView.as_view(), name="orders_list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_details"),
    path("orders/create/", OrderCreateView.as_view(), name="order_create"),
    path("orders/update/<int:pk>", OrderUpdateView.as_view(), name="order_update"),
    path("orders/delete/<int:pk>", OrderDeleteView.as_view(), name="order_delete"),
    path("orders/export/", OrdersExportView.as_view(), name="orders-export"),
]
