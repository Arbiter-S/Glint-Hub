# 3rd party library imports
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view

# Local imports
from .models import CartProduct, Cart
from .serializers import CartRetrieveSerializer, ProductCartSerializer
from utils.document import authentication_401, bad_request_400, not_found_404


# TODO: Implement changing product quantity
class CartViewSet(viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]
    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'retrieve':
            return CartRetrieveSerializer
        elif self.action == 'create':
            return ProductCartSerializer

    @extend_schema(
        summary="Returns current user's cart",
        description="""Returns a list named items including the products in current users cart with their quantity.
        
        This endpoint requires authentication.
        """,
        responses={
            200:CartRetrieveSerializer,
            401:authentication_401(),
        }

    )
    def retrieve(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=self.request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @extend_schema(
        summary="Adds a product to cart",
        description="""Adds a product to current user's cart. Returns product quantity and  its details.
        
        This endpoint requires authentication.
        """,
        request=ProductCartSerializer,
        responses={
            201 : ProductCartSerializer,
            400 : bad_request_400(),
            401 : authentication_401(),
            500 : None, # TODO: See if you can make this more detailed
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        cart = Cart.objects.get(user=user)
        serializer.validated_data['cart'] = cart
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Removes a product from cart",
        description="""Removes a product from current user's cart.
        
        This endpoint requires authentication.
        """,
        responses={
            204 : None,
            401 : authentication_401(),
            404 : not_found_404('CartProduct')
        })
    def destroy(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        cart = Cart.objects.get(user=self.request.user)
        instance = get_object_or_404(CartProduct, product=product_id, cart=cart)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)