from django.urls import path
from merchants.views import (
    MerchantProfileView,
    MerchantProductListCreateView,
    MerchantProductDetailView,
    MerchantCategoryListView,
    MerchantOrderListView,
    MerchantOrderDetailView,
    MerchantOrderFulfillView,
    MerchantCouponListCreateView,
    MerchantCouponDetailView,
    MerchantAnalyticsView,
)

urlpatterns = [
    # Profile
    path('profile/', MerchantProfileView.as_view(), name='merchant-profile'),

    # Products
    path('products/', MerchantProductListCreateView.as_view(), name='merchant-product-list'),
    path('products/<slug:slug>/', MerchantProductDetailView.as_view(), name='merchant-product-detail'),

    # Categories (read-only)
    path('categories/', MerchantCategoryListView.as_view(), name='merchant-category-list'),

    # Orders
    path('orders/', MerchantOrderListView.as_view(), name='merchant-order-list'),
    path('orders/<str:ref_code>/', MerchantOrderDetailView.as_view(), name='merchant-order-detail'),
    path('orders/<str:ref_code>/fulfill/', MerchantOrderFulfillView.as_view(), name='merchant-order-fulfill'),

    # Coupons
    path('coupons/', MerchantCouponListCreateView.as_view(), name='merchant-coupon-list'),
    path('coupons/<int:pk>/', MerchantCouponDetailView.as_view(), name='merchant-coupon-detail'),

    # Analytics
    path('analytics/', MerchantAnalyticsView.as_view(), name='merchant-analytics'),
]
