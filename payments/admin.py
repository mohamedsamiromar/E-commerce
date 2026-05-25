from django.contrib import admin
from payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'method', 'amount', 'timestamp')
    list_filter = ('method',)
    search_fields = ('user__username',)
