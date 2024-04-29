from django_filters import rest_framework as filters
from .models import Product


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr="icontains")
    category = filters.ChoiceFilter(choices=Product.categories)
    # TODO: Make a price lt and gt filter

    class Meta:
        model = Product
        fields = []
