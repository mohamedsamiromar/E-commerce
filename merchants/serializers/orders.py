from rest_framework import serializers
from merchants.models import MerchantOrderFulfillment
from orders.models import Order, OrderItem


class MerchantOrderItemSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='item.title', read_only=True)
    slug = serializers.CharField(source='item.slug', read_only=True)
    unit_price = serializers.FloatField(source='item.final_price', read_only=True)
    final_price = serializers.FloatField(source='get_final_price', read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'title', 'slug', 'quantity', 'unit_price', 'final_price')


class FulfillmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantOrderFulfillment
        fields = ('status', 'tracking_number', 'updated_at')
        read_only_fields = ('updated_at',)


class MerchantOrderSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source='user.username', read_only=True)
    my_items = serializers.SerializerMethodField()
    my_subtotal = serializers.SerializerMethodField()
    fulfillment = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id', 'ref_code', 'customer',
            'my_items', 'my_subtotal', 'fulfillment',
            'ordered_date',
        )

    def get_my_items(self, obj):
        merchant = self.context['request'].user.merchant_profile
        items = obj.items.filter(item__merchant=merchant)
        return MerchantOrderItemSerializer(items, many=True).data

    def get_my_subtotal(self, obj):
        merchant = self.context['request'].user.merchant_profile
        return sum(
            oi.get_final_price()
            for oi in obj.items.filter(item__merchant=merchant)
        )

    def get_fulfillment(self, obj):
        merchant = self.context['request'].user.merchant_profile
        try:
            fulfillment = obj.fulfillments.get(merchant=merchant)
            return FulfillmentSerializer(fulfillment).data
        except MerchantOrderFulfillment.DoesNotExist:
            return None
