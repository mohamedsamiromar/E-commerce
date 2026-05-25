from django_countries.serializer_fields import CountryField
from rest_framework import serializers
from accounts.models import Address, UserProfile


class AddressSerializer(serializers.ModelSerializer):
    country = CountryField()

    class Meta:
        model = Address
        fields = (
            'id', 'user', 'street_address', 'apartment_address',
            'country', 'zip', 'address_type', 'default',
        )
        read_only_fields = ('user',)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'stripe_customer_id', 'one_click_purchasing')
        read_only_fields = ('id', 'stripe_customer_id')
