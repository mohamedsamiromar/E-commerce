from django.urls import path
from accounts.views import (
    AddressListView,
    AddressCreateView,
    AddressUpdateView,
    AddressDeleteView,
)

urlpatterns = [
    path('addresses/', AddressListView.as_view(), name='address-list'),
    path('addresses/create/', AddressCreateView.as_view(), name='address-create'),
    path('addresses/<int:pk>/update/', AddressUpdateView.as_view(), name='address-update'),
    path('addresses/<int:pk>/delete/', AddressDeleteView.as_view(), name='address-delete'),
]
