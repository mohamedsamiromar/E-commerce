from django.contrib import admin
from catalog.models import Category, Item


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'price', 'discount_price', 'in_stock', 'category', 'created_at')
    list_filter = ('in_stock', 'category')
    search_fields = ('title', 'description')
