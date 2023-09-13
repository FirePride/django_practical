import logging

from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.syndication.views import Feed
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


from myauth.models import Profile
from .models import Product, Order


logger = logging.getLogger(__name__)


def shop_index(request: HttpRequest):
    menu = [
        ('shopapp:products_list', 'products', 'Products in the shop'),
        ('shopapp:orders_list', 'orders', 'Orders in the shop'),
    ]
    context = {
        "menu": menu,
    }
    logger.info("Rendering shop index")

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


class LatestProductsFeed(Feed):
    title = "Shop products (latest)"
    description = "Updates on changes and addition shop products"
    link = reverse_lazy("shopapp:products_list")

    @staticmethod
    def items():
        return (
            Product.objects
            .filter(archived=False)
            .order_by("-pk")[:5]
        )

    def item_title(self, item: Product):
        return item.name

    def item_description(self, item: Product):
        return item.description[:200]


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


class UserOrdersListView(UserPassesTestMixin, ListView):
    def test_func(self):
        return self.request.user.is_authenticated

    model = Order
    template_name = "shopapp/orders-from-user.html"
    context_object_name = "orders"

    def get_queryset(self):
        self.owner = get_object_or_404(User, id=self.kwargs['user_id'])
        return Order.objects.filter(user=self.owner).order_by("pk")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["owner"] = self.owner
        return context
