from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from shopapp.models import Order


# Create your tests here.
class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(
            username="test_user",
            password="Qwerty12345",
        )
        cls.user.has_perm("shopapp.view_order")

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.order = Order.objects.create(
            user=self.user,
            delivery_adress="ul. Qovunchi d.9",
            promocode="Price159"
        )

    def tearDown(self) -> None:
        self.order.delete()

    def test_order_details(self):
        response = self.client.get(reverse(
            "shopapp:order_details",
            kwargs={'pk': self.order.pk}
                    ))

        self.assertContains(response, self.order.delivery_adress)
        self.assertContains(response, self.order.promocode)

        received_data = response.context["order"].pk
        expected_data = self.order.pk
        self.assertEqual(received_data, expected_data)


class OrdersExportTestCase(TestCase):
    fixtures = [
        'users-fixture.json',
        'profiles-fixture.json',
        'products-fixture.json',
        'orders-fixture.json',
    ]

    @classmethod
    def setUpClass(cls):
        super(OrdersExportTestCase, cls).setUpClass()
        cls.user = User.objects.create_user(
            username="test_staff",
            password="Qwerty12345",
            is_staff=True
        )

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_get_orders_view(self):
        response = self.client.get(
            reverse("shopapp:orders-export")
        )
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": order.pk,
                "delivery_adress": order.delivery_adress,
                "promocode": order.promocode,
                "user": order.user.id,
                "products": [product.id for product in order.products.all()],
            }
            for order in orders
        ]
        orders_data = response.json()
        self.assertEqual(orders_data["orders"], expected_data)
