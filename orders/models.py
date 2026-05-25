import uuid

from django.contrib.auth.models import User
from django.db import models


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey('catalog.Item', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'accounts.Address', related_name='shipping_address',
        on_delete=models.SET_NULL, blank=True, null=True,
    )
    billing_address = models.ForeignKey(
        'accounts.Address', related_name='billing_address',
        on_delete=models.SET_NULL, blank=True, null=True,
    )
    payment = models.ForeignKey(
        'payments.Payment', on_delete=models.SET_NULL, blank=True, null=True,
    )
    coupon = models.ForeignKey(
        'coupons.Coupon', on_delete=models.SET_NULL, blank=True, null=True,
    )
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.ref_code or self.id} - {self.user.username}"

    def get_total(self):
        total = sum(item.get_final_price() for item in self.items.all())
        if self.coupon:
            total -= self.coupon.amount
        return max(total, 0)

    def save(self, *args, **kwargs):
        if not self.ref_code:
            self.ref_code = uuid.uuid4().hex[:12].upper()
        super().save(*args, **kwargs)
