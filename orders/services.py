from django.utils import timezone

from catalog.models import Item
from orders.models import Order, OrderItem


class CartService:
    @staticmethod
    def get_or_create_active_order(user):
        order = Order.objects.filter(user=user, ordered=False).first()
        if order:
            return order
        return Order.objects.create(user=user, ordered_date=timezone.now())

    @staticmethod
    def add_item(user, slug):
        item = Item.objects.filter(slug=slug).first()
        if not item:
            return None, "Item not found"
        order_item, _ = OrderItem.objects.get_or_create(item=item, user=user, ordered=False)
        order = CartService.get_or_create_active_order(user)
        if order.items.filter(item__slug=slug).exists():
            order_item.quantity += 1
            order_item.save()
            return order, "Item quantity updated."
        order.items.add(order_item)
        return order, "Item added to your cart."

    @staticmethod
    def remove_item(user, slug):
        item = Item.objects.filter(slug=slug).first()
        if not item:
            return None, "Item not found"
        order = Order.objects.filter(user=user, ordered=False).first()
        if not order:
            return None, "You do not have an active order"
        if not order.items.filter(item__slug=slug).exists():
            return None, "This item was not in your cart"
        order_item = OrderItem.objects.filter(item=item, user=user, ordered=False).first()
        if order_item.quantity > 1:
            order_item.quantity -= 1
            order_item.save()
        else:
            order.items.remove(order_item)
            order_item.delete()
        return order, None
