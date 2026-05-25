from django.urls import path
from orders.views import CartDetailView, CartAddView, CartRemoveView

urlpatterns = [
    path('cart/', CartDetailView.as_view(), name='cart-detail'),
    path('cart/add/', CartAddView.as_view(), name='cart-add'),
    path('cart/remove/', CartRemoveView.as_view(), name='cart-remove'),
]
