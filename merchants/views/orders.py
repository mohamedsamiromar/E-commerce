from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from merchants.models import MerchantOrderFulfillment
from merchants.permissions import IsMerchant
from merchants.serializers import MerchantOrderSerializer, FulfillmentSerializer
from orders.models import Order


def _merchant_orders_qs(merchant):
    return (
        Order.objects
        .filter(items__item__merchant=merchant, ordered=True)
        .distinct()
        .select_related('user')
        .prefetch_related('items__item', 'fulfillments')
        .order_by('-ordered_date')
    )


class MerchantOrderListView(ListAPIView):
    permission_classes = (IsMerchant,)
    serializer_class = MerchantOrderSerializer

    def get_queryset(self):
        return _merchant_orders_qs(self.request.user.merchant_profile)


class MerchantOrderDetailView(RetrieveAPIView):
    permission_classes = (IsMerchant,)
    serializer_class = MerchantOrderSerializer
    lookup_field = 'ref_code'

    def get_queryset(self):
        return _merchant_orders_qs(self.request.user.merchant_profile)


class MerchantOrderFulfillView(APIView):
    permission_classes = (IsMerchant,)

    def patch(self, request, ref_code):
        merchant = request.user.merchant_profile
        try:
            order = Order.objects.get(ref_code=ref_code, ordered=True)
        except Order.DoesNotExist:
            return Response({'message': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

        if not order.items.filter(item__merchant=merchant).exists():
            return Response({'message': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

        fulfillment, _ = MerchantOrderFulfillment.objects.get_or_create(
            merchant=merchant, order=order
        )
        serializer = FulfillmentSerializer(fulfillment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
