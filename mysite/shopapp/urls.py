from django.urls import path

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
)

app_name = "shopapp"

urlpatterns = [
    path("", shop_index, name="index"),
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
]
