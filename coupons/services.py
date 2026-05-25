from coupons.models import Coupon


class CouponService:
    @staticmethod
    def apply_coupon(user, code):
        from orders.models import Order  # local import avoids circular dependency
        order = Order.objects.filter(user=user, ordered=False).first()
        if not order:
            return None, "You do not have an active order"
        coupon = Coupon.objects.filter(code=code).first()
        if not coupon:
            return None, "Invalid coupon code"
        if not coupon.is_valid:
            return None, "This coupon is expired or inactive"
        order.coupon = coupon
        order.save()
        return order, None
