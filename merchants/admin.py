from django.contrib import admin
from merchants.models import MerchantProfile, MerchantOrderFulfillment


@admin.register(MerchantProfile)
class MerchantProfileAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'user', 'is_approved', 'created_at')
    list_filter = ('is_approved',)
    search_fields = ('store_name', 'user__username', 'user__email')
    list_editable = ('is_approved',)
    prepopulated_fields = {'store_slug': ('store_name',)}


@admin.register(MerchantOrderFulfillment)
class MerchantOrderFulfillmentAdmin(admin.ModelAdmin):
    list_display = ('merchant', 'order', 'status', 'tracking_number', 'updated_at')
    list_filter = ('status', 'merchant')
    search_fields = ('order__ref_code', 'tracking_number')
