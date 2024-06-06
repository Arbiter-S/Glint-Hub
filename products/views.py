from rest_framework.generics import ListAPIView
from .models import Product
from .serializers import ProductSerializer
from .filters import ProductFilter
from django.db.models import F
from django.core.cache import cache
from redis.exceptions import ConnectionError


class ProductListView(ListAPIView):
    serializer_class = ProductSerializer
    filterset_class = ProductFilter

    def get_queryset(self):
        try:
            price = cache.get('price', 3300000)
        # redis instance is down or not running
        except ConnectionError:
            price = 3300000
        qs = Product.objects.annotate(total_price=F('weight') * price)
        return qs
