# 3rd party library imports
from django.db.models import F
from django.core.cache import cache
from redis.exceptions import ConnectionError
from rest_framework.generics import ListAPIView, RetrieveAPIView

# Local imports
from .models import Product
from .serializers import ProductSerializer
from .filters import ProductFilter


def add_product_price(queryset=None):
    try:
        price = cache.get('price', 3300000)
    # redis instance is down or not running
    except ConnectionError:
        price = 3300000
    if queryset:
        qs = queryset.annotate(price=F('weight') * price)
    else:
        qs = Product.objects.annotate(price=F('weight') * price)
    return qs


class ProductListView(ListAPIView):
    """
    Returns a list of all products.
    This endpoint accepts url parameters.

    Returns:
        200 OK: List of Product objects

    """
    serializer_class = ProductSerializer
    filterset_class = ProductFilter

    def get_queryset(self):
        return add_product_price()


class ProductView(RetrieveAPIView):
    """
    Returns a single Product object.
    Product ID is required in the URL.

    Returns:
        200 OK: Product object
        404 Not Found: No product found with the requested ID
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        return add_product_price()
