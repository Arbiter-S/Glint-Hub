from .models import Product
from django_filters import rest_framework as filters


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    category = filters.ChoiceFilter(choices=Product.categories)
    price_range = filters.RangeFilter(
        field_name="total_price", lookup_expr="range", label="Price Range"
    )
    # TODO: price range type is not clear for drf-spectacular auto schema generation. See if there is a way to fix it

    class Meta:
        model = Product
        fields = []
