from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django_countries.fields import CountryField


ADDRESS_TYPE_CHOICES = (
    ('S', 'Shipping'),
    ('B', 'Billing'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_TYPE_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.street_address}, {self.country}"

    class Meta:
        verbose_name_plural = 'Addresses'


def _create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(_create_user_profile, sender=User)
