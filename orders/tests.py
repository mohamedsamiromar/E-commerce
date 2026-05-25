from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from catalog.models import Item
from coupons.models import Coupon
from orders.models import Order, OrderItem
from orders.services import CartService


class CartServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.item = Item.objects.create(
            title="Product", price=25.00, slug="product", description="A product"
        )

    def test_add_item_creates_order(self):
        order, message = CartService.add_item(self.user, "product")
        self.assertIsNotNone(order)
        self.assertFalse(order.ordered)
        self.assertEqual(order.items.count(), 1)

    def test_add_item_increases_quantity(self):
        CartService.add_item(self.user, "product")
        order, _ = CartService.add_item(self.user, "product")
        self.assertEqual(order.items.first().quantity, 2)

    def test_add_nonexistent_item(self):
        result, message = CartService.add_item(self.user, "nonexistent")
        self.assertIsNone(result)
        self.assertEqual(message, "Item not found")

    def test_remove_item_decreases_quantity(self):
        CartService.add_item(self.user, "product")
        CartService.add_item(self.user, "product")
        CartService.remove_item(self.user, "product")
        order_item = OrderItem.objects.get(user=self.user, item=self.item, ordered=False)
        self.assertEqual(order_item.quantity, 1)

    def test_remove_item_deletes_when_quantity_one(self):
        CartService.add_item(self.user, "product")
        CartService.remove_item(self.user, "product")
        self.assertFalse(
            OrderItem.objects.filter(user=self.user, item=self.item, ordered=False).exists()
        )

    def test_remove_from_empty_cart(self):
        _, error = CartService.remove_item(self.user, "product")
        self.assertEqual(error, "You do not have an active order")


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="orderuser", password="password")
        self.item = Item.objects.create(
            title="Widget", price=30.00, slug="widget", description="A widget"
        )

    def test_order_total_without_coupon(self):
        order = Order.objects.create(user=self.user, ordered_date=timezone.now())
        order_item = OrderItem.objects.create(user=self.user, item=self.item, quantity=2)
        order.items.add(order_item)
        self.assertEqual(order.get_total(), 60.00)

    def test_order_total_with_coupon(self):
        coupon = Coupon.objects.create(code="FIVE", amount=5.00)
        order = Order.objects.create(user=self.user, ordered_date=timezone.now())
        order_item = OrderItem.objects.create(user=self.user, item=self.item, quantity=1)
        order.items.add(order_item)
        order.coupon = coupon
        order.save()
        self.assertEqual(order.get_total(), 25.00)

    def test_order_total_never_negative(self):
        coupon = Coupon.objects.create(code="BIG", amount=100.00)
        order = Order.objects.create(user=self.user, ordered_date=timezone.now())
        order_item = OrderItem.objects.create(user=self.user, item=self.item, quantity=1)
        order.items.add(order_item)
        order.coupon = coupon
        order.save()
        self.assertEqual(order.get_total(), 0.00)

    def test_auto_ref_code_generated(self):
        order = Order.objects.create(user=self.user, ordered_date=timezone.now())
        self.assertIsNotNone(order.ref_code)
        self.assertEqual(len(order.ref_code), 12)
