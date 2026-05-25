from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from coupons.models import Coupon
from coupons.services import CouponService
from catalog.models import Item
from orders.services import CartService


class CouponModelTest(TestCase):
    def test_active_coupon_is_valid(self):
        coupon = Coupon.objects.create(code="SAVE10", amount=10.00, active=True)
        self.assertTrue(coupon.is_valid)

    def test_inactive_coupon_not_valid(self):
        coupon = Coupon.objects.create(code="OFF", amount=5.00, active=False)
        self.assertFalse(coupon.is_valid)

    def test_expired_coupon_not_valid(self):
        past = timezone.now() - timezone.timedelta(days=1)
        coupon = Coupon.objects.create(code="EXPIRED", amount=5.00, valid_to=past)
        self.assertFalse(coupon.is_valid)

    def test_future_coupon_not_valid(self):
        future = timezone.now() + timezone.timedelta(days=1)
        coupon = Coupon.objects.create(code="FUTURE", amount=5.00, valid_from=future)
        self.assertFalse(coupon.is_valid)


class CouponServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="couponuser", password="password")
        self.coupon = Coupon.objects.create(code="SAVE10", amount=10.00)
        self.item = Item.objects.create(
            title="Item", price=50.00, slug="item", description="Item"
        )

    def test_apply_coupon(self):
        CartService.add_item(self.user, "item")
        order, error = CouponService.apply_coupon(self.user, "SAVE10")
        self.assertIsNone(error)
        order.refresh_from_db()
        self.assertEqual(order.coupon, self.coupon)
        self.assertEqual(order.get_total(), 40.00)

    def test_apply_invalid_coupon(self):
        CartService.add_item(self.user, "item")
        _, error = CouponService.apply_coupon(self.user, "INVALID")
        self.assertEqual(error, "Invalid coupon code")

    def test_apply_inactive_coupon(self):
        inactive = Coupon.objects.create(code="INACTIVE", amount=5.00, active=False)
        CartService.add_item(self.user, "item")
        _, error = CouponService.apply_coupon(self.user, "INACTIVE")
        self.assertIn("expired or inactive", error)

    def test_apply_coupon_no_active_order(self):
        _, error = CouponService.apply_coupon(self.user, "SAVE10")
        self.assertEqual(error, "You do not have an active order")
