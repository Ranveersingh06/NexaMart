import django_filters
from .models import Product

# ============================================================
# PRODUCT FILTER
# ============================================================
# Why: Allows filtering products by category, price,
# brand, rating etc from API query params
# Example: /api/products/?category=1&min_price=100&max_price=500
class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte'
    )
    max_price = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte'
    )
    category = django_filters.NumberFilter(
        field_name='category__id'
    )
    brand = django_filters.CharFilter(
        field_name='brand',
        lookup_expr='icontains'
    )
    min_rating = django_filters.NumberFilter(
        field_name='average_rating',
        lookup_expr='gte'
    )
    in_stock = django_filters.BooleanFilter(
        field_name='stock',
        method='filter_in_stock'
    )

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__gt=0)
        return queryset

    class Meta:
        model = Product
        fields = [
            'category', 'brand',
            'min_price', 'max_price',
            'min_rating', 'in_stock',
            'is_featured'
        ]