from django_countries.serializer_fields import CountryField
from rest_framework import serializers
from project.models import Item, Order, OrderItem, Coupon, Address


class StringSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = (
            "titie",
            "price",
            "discount_price",
            "slug",
            "description",
            "quantity",
        )

    def get_category(self, obj):
        return obj.get_category_display()

    def get_label(self, obj):
        return obj.get_label_display()


class OrderItemSerializer(serializers.ModelSerializer):
    item_variations = serializers.SerializerMethodField()
    item = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = (
            'id',
            'item',
            'item_variations',
            'quantity',
            'final_price'
        )

    def get_item(self, obj):
        return ItemSerializer(obj.item).data


class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    coupon = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id',
            'order_items',
            'total',
            'coupon'
        )

    def get_order_items(self, obj):
        return OrderItemSerializer(obj.items.all(), many=True).data

    def get_total(self, obj):
        return obj.get_total()

    def get_coupone(self, obj):
        if obj.Coupon is not None:
            return CouponSerializer(obj.Coupon)
        return None


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields={
            'id',
            'code',
            'amount'}


class AddressSerializer(serializers.ModelSerializer):
    country = CountryField()

    class Meta:
        model = Address
        fields = (
            'id',
            'user',
            'street_address',
            'apartment_address',
            'country',
            'zip',
            'address_type',
            'default'
        )
