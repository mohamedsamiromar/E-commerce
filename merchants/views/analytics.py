from django.db.models import Sum, Count, Q
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.models import Item
from merchants.models import MerchantOrderFulfillment
from merchants.permissions import IsMerchant
from orders.models import Order


class MerchantAnalyticsView(APIView):
    permission_classes = (IsMerchant,)

    def get(self, request):
        merchant = request.user.merchant_profile

        products_qs = Item.objects.filter(merchant=merchant)
        orders_qs = Order.objects.filter(
            items__item__merchant=merchant, ordered=True
        ).distinct()

        total_revenue = sum(
            sum(oi.get_final_price() for oi in order.items.filter(item__merchant=merchant))
            for order in orders_qs.prefetch_related('items__item')
        )

        pending_count = MerchantOrderFulfillment.objects.filter(
            merchant=merchant,
            status=MerchantOrderFulfillment.STATUS_PENDING,
        ).count()

        low_stock_products = products_qs.filter(
            stock_qty__isnull=False, stock_qty__lte=5
        ).values('id', 'title', 'slug', 'stock_qty')

        top_products = (
            products_qs
            .annotate(units_sold=Sum('orderitem__quantity', filter=Q(orderitem__ordered=True)))
            .order_by('-units_sold')
            .values('id', 'title', 'slug', 'units_sold')[:5]
        )

        return Response({
            'total_revenue': round(total_revenue, 2),
            'orders_count': orders_qs.count(),
            'pending_orders': pending_count,
            'products_count': products_qs.count(),
            'low_stock_products': list(low_stock_products),
            'top_products': list(top_products),
        })
