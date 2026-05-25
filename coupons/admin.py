from django.contrib import admin
from coupons.models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'amount', 'active', 'valid_from', 'valid_to')
    list_filter = ('active',)
