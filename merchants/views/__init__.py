from merchants.views.profile import MerchantProfileView
from merchants.views.products import (
    MerchantProductListCreateView,
    MerchantProductDetailView,
    MerchantCategoryListView,
)
from merchants.views.orders import (
    MerchantOrderListView,
    MerchantOrderDetailView,
    MerchantOrderFulfillView,
)
from merchants.views.coupons import MerchantCouponListCreateView, MerchantCouponDetailView
from merchants.views.analytics import MerchantAnalyticsView

__all__ = [
    'MerchantProfileView',
    'MerchantProductListCreateView',
    'MerchantProductDetailView',
    'MerchantCategoryListView',
    'MerchantOrderListView',
    'MerchantOrderDetailView',
    'MerchantOrderFulfillView',
    'MerchantCouponListCreateView',
    'MerchantCouponDetailView',
    'MerchantAnalyticsView',
]
