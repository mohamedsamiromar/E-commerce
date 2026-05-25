from rest_framework import serializers
from catalog.models import Category, Item


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True, required=False)
    final_price = serializers.FloatField(read_only=True)
    has_discount = serializers.BooleanField(read_only=True)

    class Meta:
        model = Item
        fields = (
            'id', 'title', 'price', 'discount_price', 'final_price',
            'has_discount', 'slug', 'description', 'image',
            'category', 'category_id', 'in_stock', 'created_at',
        )
