from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from coupons.models import Coupon
from merchants.permissions import IsMerchant
from merchants.serializers import MerchantCouponSerializer


class MerchantCouponListCreateView(ListCreateAPIView):
    permission_classes = (IsMerchant,)
    serializer_class = MerchantCouponSerializer

    def get_queryset(self):
        return Coupon.objects.filter(merchant=self.request.user.merchant_profile)

    def perform_create(self, serializer):
        serializer.save(merchant=self.request.user.merchant_profile)


class MerchantCouponDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsMerchant,)
    serializer_class = MerchantCouponSerializer
    http_method_names = ('get', 'patch', 'delete')

    def get_queryset(self):
        return Coupon.objects.filter(merchant=self.request.user.merchant_profile)
