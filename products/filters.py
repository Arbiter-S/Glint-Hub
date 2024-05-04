from django_filters import rest_framework as filters
from .models import Product
from django.core.cache import cache
from django.db.models import F


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr="icontains")
    category = filters.ChoiceFilter(choices=Product.categories)
    price_range = filters.RangeFilter(field_name='total_price', lookup_expr='range', label='Price Range')

    class Meta:
        model = Product
        fields = []
