from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from myauth.models import Profile
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


def shop_index(request: HttpRequest):
    menu = [
        ('shopapp:products_list', 'products', 'Products in the shop'),
        ('shopapp:orders_list', 'orders', 'Orders in the shop'),
    ]
    context = {
        "menu": menu,
    }
    return render(request, 'shopapp/shop-index.html', context=context)


class ProductDetailView(DetailView):
    template_name = 'shopapp/products-details.html'
    queryset = Product.objects.filter(archived=False)
    context_object_name = 'product'


class ProductListView(ListView):
    template_name = 'shopapp/products-list.html'
    queryset = Product.objects.filter(archived=False)
    context_object_name = "products"


class ProductCreateView(PermissionRequiredMixin, CreateView):
    request: HttpRequest
    permission_required = 'shopapp.add_product'
    model = Product
    fields = "name", "price", "description", "discount"
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        form.instance.created_by = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        print(self.get_object().created_by)
        if self.request.user.is_superuser or (
                self.request.user.has_perms(['shopapp.change_product'])
                and Profile.objects.get(user=self.request.user) == self.get_object().created_by):
            return True
        return False

    model = Product
    fields = "name", "price", "description", "discount"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:products_details",
            kwargs={"pk": self.object.pk}
        )


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrdersListView(ListView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


class OrderDetailView(DetailView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


class OrderCreateView(CreateView):
    model = Order
    fields = "user", "products", "delivery_adress", "promocode"
    success_url = reverse_lazy("shopapp:orders_list")


class OrderUpdateView(UpdateView):
    model = Order
    fields = "user", "products", "delivery_adress", "promocode"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:order_details",
            kwargs={"pk": self.object.pk}
        )


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("shopapp:orders_list")


class OrdersExportView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    @staticmethod
    def get(request: HttpRequest) -> JsonResponse:
        orders = Order.objects.order_by("pk").all()
        orders_data = [
            {
                "pk": order.pk,
                "delivery_adress": order.delivery_adress,
                "promocode": order.promocode,
                "user": order.user.id,
                "products": [product.id for product in order.products.all()],
            }
            for order in orders
        ]

        return JsonResponse({"orders": orders_data})
