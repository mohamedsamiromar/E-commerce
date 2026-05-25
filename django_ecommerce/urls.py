from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/auth/token/', obtain_auth_token, name='api_token_auth'),
    path('allauth/', include('allauth.urls')),
    # Feature apps
    path('api/catalog/', include('catalog.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/coupons/', include('coupons.urls')),
    # Merchant dashboard
    path('api/merchant/', include('merchants.urls')),
]
