from django.urls import path
from catalog.views import ItemListCreateView

urlpatterns = [
    path('items/', ItemListCreateView.as_view(), name='item-list-create'),
]
