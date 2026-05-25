from django.contrib.auth.models import User
from django.db import models


class Payment(models.Model):
    METHOD_CHOICES = (
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
        ('apple_pay', 'Apple Pay'),
        ('google_pay', 'Google Pay'),
    )
    stripe_charge_id = models.CharField(max_length=50, blank=True, null=True)
    paypal_payment_id = models.CharField(max_length=50, blank=True, null=True)
    method = models.CharField(max_length=10, choices=METHOD_CHOICES, default='stripe')
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        username = self.user.username if self.user else 'Anonymous'
        return f"{self.method}: {self.amount} - {username}"
