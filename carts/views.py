# 3rd party library imports
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.shortcuts import get_object_or_404


# Local imports
from .models import CartProduct, Cart
from .serializers import CartRetrieveSerializer, ProductCartSerializer


class CartViewSet(viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]
    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'retrieve':
            return CartRetrieveSerializer
        elif self.action == 'create':
            return ProductCartSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Returns:
            200 OK: Gives a list named items including the product details and quantity in current user's cart
            401 Unauthorized: if authentication fails.
        """
        cart = Cart.objects.get(user=self.request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Adds a product to current user's cart.
        This endpoint requires authentication.

        Request Body:
            product_id (int): ID of the product to add
            product_quantity (int): Number of products to add

        Returns:
            201 Created: Quantity and details of the added product
            400 Bad Request: If request body's format is incorrect or a product with that id is not found.
            401 Unauthorized: If authentication fails.
            500 Internal Server Error: If user already has that product in their cart.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        cart = Cart.objects.get(user=user)
        serializer.validated_data['cart'] = cart
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """
        Removes a product from current user's cart.
        This endpoint requires authentication.

        Returns:
            204 No Content: Product is successfully removed from current user's cart.
            401 Unauthorized: If authentication fails.
            404 Not Found: If the product does not exist in the user's cart.
        """
        product_id = kwargs.get('product_id')
        cart = Cart.objects.get(user=self.request.user)
        instance = get_object_or_404(CartProduct, product=product_id, cart=cart)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)