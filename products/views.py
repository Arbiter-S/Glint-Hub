# 3rd party library imports
from rest_framework.generics import ListAPIView, RetrieveAPIView

# Local imports
from .serializers import ProductSerializer
from .filters import ProductFilter
from .utils import add_product_field


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
        return add_product_field()


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
        return add_product_field()
