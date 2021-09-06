"""django_ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from project.views import ItemViewListCreate, OrderDetailView, AddToCart, PaymentView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('login', views.obtain_auth_token, name='api_token_auth'),

    path('allauth', include('allauth.urls')),
    path('item-list-create', ItemViewListCreate.as_view(), name='item-list-create'),
    path('order-details', OrderDetailView.as_view(), name='order-details'),
    path('add-to-cart', AddToCart.as_view(), name='Add-to-cart'),
    path('check-out', PaymentView.as_view(), name='check-out'),

]
