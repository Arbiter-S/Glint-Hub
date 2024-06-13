# 3rd party library imports
from django.db.models import F
from django.core.cache import cache
from redis.exceptions import ConnectionError
from rest_framework.generics import ListAPIView, RetrieveAPIView

# Local imports
from .models import Product
from .serializers import ProductSerializer
from .filters import ProductFilter


def add_product_price():
    try:
        price = cache.get('price', 3300000)
    # redis instance is down or not running
    except ConnectionError:
        price = 3300000
    qs = Product.objects.annotate(total_price=F('weight') * price)
    return qs


class ProductListView(ListAPIView):
    serializer_class = ProductSerializer
    filterset_class = ProductFilter

    def get_queryset(self):
        return add_product_price()


class ProductView(RetrieveAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return add_product_price()
