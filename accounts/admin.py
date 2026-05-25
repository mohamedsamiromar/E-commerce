from django.contrib import admin
from accounts.models import Address, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'stripe_customer_id', 'one_click_purchasing')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'street_address', 'country', 'address_type', 'default')
    list_filter = ('address_type', 'default', 'country')
