from rest_framework.generics import RetrieveUpdateAPIView
from merchants.permissions import IsMerchant
from merchants.serializers import MerchantProfileSerializer


class MerchantProfileView(RetrieveUpdateAPIView):
    permission_classes = (IsMerchant,)
    serializer_class = MerchantProfileSerializer
    http_method_names = ('get', 'patch')

    def get_object(self):
        return self.request.user.merchant_profile
