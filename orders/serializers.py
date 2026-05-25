from rest_framework import serializers

from catalog.serializers import ItemSerializer
from coupons.serializers import CouponSerializer
from orders.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    final_price = serializers.FloatField(read_only=True, source='get_final_price')

    class Meta:
        model = OrderItem
        fields = ('id', 'item', 'quantity', 'final_price')


class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()
    total = serializers.FloatField(read_only=True, source='get_total')
    coupon = CouponSerializer(read_only=True)

    class Meta:
        model = Order
        fields = (
            'id', 'ref_code', 'order_items', 'total', 'coupon',
            'being_delivered', 'received', 'ordered_date',
        )

    def get_order_items(self, obj):
        return OrderItemSerializer(obj.items.all(), many=True).data
