# 3rd party library imports
# Local imports
from .models import Cart, CartProduct
from .serializers import (
    CartRetrieveSerializer,
    CartUpdateSerializer,
    ProductCartSerializer,
)
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiResponse, extend_schema
from logging import getLogger
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from utils.document import authentication_401, bad_request_400, not_found_404

logger = getLogger(__name__)


class CartViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self, *args, **kwargs):
        if self.action == "retrieve":
            return CartRetrieveSerializer
        elif self.action == "create":
            return ProductCartSerializer
        elif self.action == "update":
            return CartUpdateSerializer

    @extend_schema(
        summary="Returns current user's cart",
        description="""Returns a list named items including the products in current users cart with their quantity.
        
        This endpoint requires authentication.
        """,
        responses={
            200: CartRetrieveSerializer,
            401: authentication_401(),
        },
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
            201: ProductCartSerializer,
            400: bad_request_400(),
            401: authentication_401(),
            500: OpenApiResponse(
                response=None,
                description="Product is already in the cart or"
                " product with that id does not exist",
            ),
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        cart = Cart.objects.get(user=user)
        serializer.validated_data["cart"] = cart
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Removes a product from cart",
        description="""Removes a product from current user's cart.
        
        This endpoint requires authentication.
        """,
        responses={
            204: None,
            401: authentication_401(),
            404: not_found_404("CartProduct"),
        },
    )
    def destroy(self, request, *args, **kwargs):
        product_id = kwargs.get("product_id")
        cart = Cart.objects.get(user=self.request.user)
        instance = get_object_or_404(CartProduct, product=product_id, cart=cart)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        summary="Updates a product's quantity in the cart",
        description="""Updates quantity of a product in current user's cart.
        
        This endpoint requires authentication.""",
        request=CartUpdateSerializer,
        responses={
            200: CartUpdateSerializer,
            400: bad_request_400(),
            401: authentication_401(),
            404: not_found_404("CartProduct"),
        },
    )
    def update(
        self, request, *args, **kwargs
    ):  # TODO: Check if patch requests with no body should return a 400 error
        product_id = kwargs.get("product_id")
        cart = Cart.objects.get(user=self.request.user)
        instance = get_object_or_404(CartProduct, product=product_id, cart=cart)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
