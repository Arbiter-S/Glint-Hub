# 3rd party library imports
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# Local imports
from .models import Cart
from .serializers import CartSerializer
from products.serializers import ProductAddCartSerializer


class CartView(RetrieveAPIView):
    """
    Shows current user's cart.
    This endpoint requires authentication.


    Returns:
        200 OK: Current user's Cart object
        401 Unauthorized: if authentication fails.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_object(self):
        return Cart.objects.get(user=self.request.user)


class CartAdd(CreateAPIView):
    """
    Adds a product to current user's cart.
    This endpoint requires authentication.

    Request Body:
        product_id (int): ID of the product to add

    Returns:
        201 Created: product id of the added product
        401 Unauthorized: if authentication fails.
        400 Bad Request: if body's format is incorrect or a product with that id is not found.
    """
    queryset = Cart.products.through.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProductAddCartSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        cart = Cart.objects.filter(user=user).first()
        serializer.validated_data['cart'] = cart
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
