from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny
from catalog.filters import ItemFilter
from catalog.models import Item
from catalog.serializers import ItemSerializer


class ItemListCreateView(ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ItemSerializer
    filterset_class = ItemFilter
    search_fields = ('title', 'description')
    ordering_fields = ('title', 'price', 'id')
    queryset = Item.objects.select_related('category').all()
