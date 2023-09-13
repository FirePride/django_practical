from io import TextIOWrapper
from csv import DictReader

from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path

from .models import Product, Order
from .admin_mixins import ExportAsCSVMixin
from .forms import CSVImportForm


class OrderInline(admin.TabularInline):
    model = Product.orders.through


@admin.action(description="Archive products")
def make_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description="Unarchive products")
def make_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [
        make_archived,
        make_unarchived,
        'export_csv',
    ]
    inlines = [
        OrderInline,
    ]
    list_display = 'pk', 'name', 'description_short', 'price', 'discount', 'archived'
    list_display_links = 'pk', 'name'
    ordering = 'pk',
    search_fields = 'name', 'price'
    fieldsets = [
        (None, {
            "fields": ("name", "description"),
        }),
        ("Price options", {
            "fields": ("price", "discount"),
            "classes": ("wide", "collapse"),
        }),
        ("Extra options", {
            "fields": ("archived",),
            "classes": ("collapse",),
            "description": "Extra options. Field 'archived' is for soft delete."
        }),
    ]

    @staticmethod
    def description_short(obj: Product) -> str:
        if len(obj.description) < 50:
            return obj.description
        return obj.description[:48] + '...'


class ProductInline(admin.StackedInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    change_list_template = "shopapp/orders_changelist.html"
    inlines = [
        ProductInline,
    ]
    list_display = 'pk', 'user_verbose', 'delivery_adress', 'promocode'
    list_display_links = 'pk', 'user_verbose'
    ordering = 'pk',
    search_fields = 'user', 'promocode'

    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related("products")

    @staticmethod
    def user_verbose(obj: Order) -> str:
        return obj.user.first_name or obj.user.username

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVImportForm()
            context = {
                "form": form,
            }
            return render(request, "admin/csv-form.html", context)

        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "admin/csv-form.html", context, status=400)

        csv_file = TextIOWrapper(
            form.files["csv_file"].file,
            encoding=request.encoding
        )

        reader = DictReader(csv_file)

        orders_list = [
            row
            for row in reader
        ]

        for order_info in orders_list:
            order = Order.objects.create(
                user=User.objects.get(username=order_info["user"]),
                delivery_adress=order_info["delivery_adress"],
                promocode=order_info["promocode"]
            )

            products = [
                int(i_product)
                for i_product in order_info["products"].split()
            ]

            for i_product in products:
                order.products.add(i_product)

        self.message_user(request, "Data from CSV was imported")
        return redirect("..")

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                "import-orders-csv/",
                self.import_csv,
                name="import-orders-csv"
            )
        ]
        return new_urls + urls
