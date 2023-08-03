from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from myauth.models import Profile


class Product(models.Model):
    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")

    name = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    created_by = models.ForeignKey(Profile, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f'{self.pk}. "{self.name}"'


class Order(models.Model):
    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")

    delivery_adress = models.TextField(null=False, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name="orders")

    def __str__(self) -> str:
        return f'{self.pk}. {self.user}'
