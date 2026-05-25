from django.contrib.auth.models import User
from django.db import models


class MerchantProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='merchant_profile'
    )
    store_name = models.CharField(max_length=100)
    store_slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='merchant_logos/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.store_name


class MerchantOrderFulfillment(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_PROCESSING = 'processing'
    STATUS_SHIPPED = 'shipped'
    STATUS_DELIVERED = 'delivered'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_PROCESSING, 'Processing'),
        (STATUS_SHIPPED, 'Shipped'),
        (STATUS_DELIVERED, 'Delivered'),
        (STATUS_CANCELLED, 'Cancelled'),
    )

    merchant = models.ForeignKey(
        MerchantProfile, on_delete=models.CASCADE, related_name='fulfillments'
    )
    order = models.ForeignKey(
        'orders.Order', on_delete=models.CASCADE, related_name='fulfillments'
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    tracking_number = models.CharField(max_length=100, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('merchant', 'order')

    def __str__(self):
        return f"{self.merchant.store_name} — Order {self.order.ref_code} [{self.status}]"
