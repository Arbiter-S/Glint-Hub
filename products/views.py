# 3rd party library imports
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet

# Local imports
from .serializers import ProductSerializer
from .filters import ProductFilter
from .utils import add_product_field


class ProductViewSet(ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    filterset_class = ProductFilter

    def get_queryset(self):
        return add_product_field()

