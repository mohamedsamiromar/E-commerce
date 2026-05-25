from rest_framework import serializers
from catalog.models import Category, Item


class MerchantCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class MerchantProductSerializer(serializers.ModelSerializer):
    category = MerchantCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False,
        allow_null=True,
    )
    final_price = serializers.FloatField(read_only=True)
    has_discount = serializers.BooleanField(read_only=True)

    class Meta:
        model = Item
        fields = (
            'id', 'title', 'slug', 'description', 'image',
            'price', 'discount_price', 'final_price', 'has_discount',
            'category', 'category_id',
            'in_stock', 'stock_qty',
            'created_at', 'updated_at',
        )
        read_only_fields = ('created_at', 'updated_at')
