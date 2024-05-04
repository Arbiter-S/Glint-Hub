from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Product
from .serializers import ProductSerializer
from .filters import ProductFilter
from django.db.models import F
from django.core.cache import cache


# Create your views here.

class ProductListView(ListAPIView):
    serializer_class = ProductSerializer
    filterset_class = ProductFilter

    # TODO: This view should also have the price
    def get_queryset(self):
        price = cache.get('price')
        qs = Product.objects.annotate(total_price=F('weight') * price)
        return qs
