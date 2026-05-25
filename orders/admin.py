from django.contrib import admin
from orders.models import Order, OrderItem


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('item', 'user', 'quantity', 'ordered')
    list_filter = ('ordered',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('ref_code', 'user', 'ordered', 'being_delivered', 'received', 'payment_method')
    list_filter = ('ordered', 'being_delivered', 'received')

    @admin.display(description='Payment')
    def payment_method(self, obj):
        if obj.payment:
            return f"{obj.payment.get_method_display()} (${obj.payment.amount})"
        return '-'
