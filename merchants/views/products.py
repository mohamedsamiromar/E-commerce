from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from catalog.models import Category, Item
from merchants.permissions import IsMerchant
from merchants.serializers import MerchantProductSerializer, MerchantCategorySerializer


class MerchantProductListCreateView(ListCreateAPIView):
    permission_classes = (IsMerchant,)
    serializer_class = MerchantProductSerializer

    def get_queryset(self):
        return Item.objects.filter(
            merchant=self.request.user.merchant_profile
        ).select_related('category').order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(merchant=self.request.user.merchant_profile)


class MerchantProductDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsMerchant,)
    serializer_class = MerchantProductSerializer
    lookup_field = 'slug'
    http_method_names = ('get', 'patch', 'delete')

    def get_queryset(self):
        return Item.objects.filter(merchant=self.request.user.merchant_profile)


class MerchantCategoryListView(ListAPIView):
    permission_classes = (IsMerchant,)
    serializer_class = MerchantCategorySerializer
    queryset = Category.objects.all().order_by('name')
