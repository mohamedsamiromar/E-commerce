from django.urls import path
from coupons.views import ApplyCouponView

urlpatterns = [
    path('apply/', ApplyCouponView.as_view(), name='apply-coupon'),
]
