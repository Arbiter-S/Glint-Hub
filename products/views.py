# 3rd party library imports
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ReadOnlyModelViewSet
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.pagination import PageNumberPagination

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

    class ProductPagination(PageNumberPagination):
        page_size = 25
        last_page_strings = ['last_page', 'last']

    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = ['price', 'created_at']
    pagination_class = ProductPagination

    def get_queryset(self):
        return add_price_field().order_by('id')

