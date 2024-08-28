# 3rd party library imports
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# Local imports
from .models import CartProduct, Cart
from .serializers import CartSerializer, ProductCartSerializer


class CartView(RetrieveAPIView):
    """
    Shows items in current user's cart.
    This endpoint requires authentication.


    Returns:
        200 OK: Gives a list named items including the product id and quantity in current user's cart
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
        product_quantity (int): Number of products to add

    Returns:
        201 Created: product id and quantity of the added product
        400 Bad Request: If body's format is incorrect or a product with that id is not found.
        401 Unauthorized: If authentication fails.
        500 Internal Server Error: If user already has that product in their cart.
    """
    queryset = CartProduct.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProductCartSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        cart = Cart.objects.get(user=user)
        serializer.validated_data['cart'] = cart
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
