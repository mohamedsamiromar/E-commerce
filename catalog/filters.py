import django_filters
from django.db.models import Q
from catalog.models import Item


class ItemFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    has_discount = django_filters.BooleanFilter(
        field_name='discount_price', lookup_expr='isnull', exclude=True
    )
    category = django_filters.CharFilter(field_name='category__slug')
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Item
        fields = ('min_price', 'max_price', 'has_discount', 'category')

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | Q(description__icontains=value)
        )
