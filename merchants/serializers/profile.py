from rest_framework import serializers
from merchants.models import MerchantProfile


class MerchantProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantProfile
        fields = ('id', 'store_name', 'store_slug', 'description', 'logo', 'is_approved', 'created_at')
        read_only_fields = ('is_approved', 'created_at')
