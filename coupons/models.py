from django.db import models
from django.utils import timezone


class Coupon(models.Model):
    merchant = models.ForeignKey(
        'merchants.MerchantProfile',
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='coupons',
    )
    code = models.CharField(max_length=15, unique=True)
    amount = models.FloatField()
    active = models.BooleanField(default=True)
    valid_from = models.DateTimeField(blank=True, null=True)
    valid_to = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.code

    @property
    def is_valid(self):
        now = timezone.now()
        if self.valid_from and now < self.valid_from:
            return False
        if self.valid_to and now > self.valid_to:
            return False
        return self.active
