# 3rd party library imports
from rest_framework.viewsets import ReadOnlyModelViewSet
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.serializers import CharField

# Local imports
from .serializers import ProductSerializer
from .filters import ProductFilter
from utils.product import add_price_field
from utils.document import not_found_404

@extend_schema_view(
    retrieve=extend_schema(
        summary="Returns a product's details",
        description="""Returns details of a product object 
        including all its fields with its current price""",
        responses={
            200: ProductSerializer,
            404: not_found_404('Product'),
        }
    ),
    list=extend_schema(
        summary="Returns a list of products",
        description="""Returns a list of product objects 
        including all their fields with their current price""",
        responses={
            200: ProductSerializer,
        }
))
class ProductViewSet(ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    filterset_class = ProductFilter

    def get_queryset(self):
        return add_price_field()

