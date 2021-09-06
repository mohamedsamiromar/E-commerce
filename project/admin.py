from django.contrib import admin
from project.models import OrderItem,Item ,Order

admin.site.register(Order)
admin.site.register(Item)
admin.site.register(OrderItem)
