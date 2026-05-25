from rest_framework import serializers
from coupons.models import Coupon


class MerchantCouponSerializer(serializers.ModelSerializer):
    is_valid = serializers.BooleanField(read_only=True)

    class Meta:
        model = Coupon
        fields = ('id', 'code', 'amount', 'active', 'valid_from', 'valid_to', 'is_valid')
