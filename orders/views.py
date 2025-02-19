# 3rd party library imports
from django.db import DatabaseError, transaction
from drf_spectacular.utils import extend_schema, extend_schema_view
from logging import getLogger

# Local imports
from orders.models import Order, OrderProduct
from orders.serializers import OrderListSerializer, OrderRetrieveSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from utils.document import authentication_401, bad_request_400, not_found_404
from utils.product import add_price_field

logger = getLogger(__name__)


@extend_schema_view(
    list=extend_schema(
        summary="Returns a list of orders",
        description="""Returns a simplified list of orders for the current user.
        
        This endpoint requires authentication.""",
        responses={
            200: OrderListSerializer,
            401: authentication_401(),
        },
    ),
    retrieve=extend_schema(
        summary="Returns an Order object",
        description="""Returns a more detailed representation of an Order object
        
        This endpoint requires authentication.""",
        responses={
            200: OrderRetrieveSerializer,
            401: authentication_401(),
            404: not_found_404("Order"),
        },
    ),
    partial_update=extend_schema(
        summary="Updates info on an order",
        description="""Updates note and address fields on an Order object.
        
        This endpoint requires authentication.""",
        responses={
            200: OrderRetrieveSerializer,
            401: authentication_401(),
            400: bad_request_400(),
            404: not_found_404("Order"),
        },
    ),
)
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", "head", "options", "trace"]

    def get_queryset(self):
        user = self.request.user  # TODO: Consider changing for invalid status
        qs = Order.objects.filter(user=user)
        return qs

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        return OrderRetrieveSerializer

    @extend_schema(
        summary="Creates an order",
        description="""Creates an order from products in user's cart and removes products from the cart.
        
        This endpoint requires authentication. """,
        request=OrderRetrieveSerializer,
        responses={
            201: OrderRetrieveSerializer,
            400: bad_request_400(),
            401: authentication_401(),
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        address = serializer.validated_data.get("address")
        note = serializer.validated_data.get("note", None)
        try:
            with transaction.atomic():
                # getting the fields
                user = self.request.user
                cart = user.cart
                products = add_price_field(cart.products.all())
                cart_products = cart.cartproduct_set.all()
                # calculating total price of the cart items

                total_price = 0
                for cart_product in cart_products:
                    product_id = cart_product.product.id
                    product = products.get(pk=product_id)
                    quantity = cart_product.product_quantity
                    price = product.price * quantity
                    total_price += price

                order = Order(
                    user=user, total_price=total_price, address=address, note=note
                )
                order.save()
                for (
                    cart_product
                ) in cart_products:  # This section populates products field of an order
                    # getting the price for each item in the order
                    product_id = cart_product.product.id
                    product = products.get(pk=product_id)
                    price = product.price

                    order_product = OrderProduct(
                        order=order,
                        product=cart_product.product,
                        product_quantity=cart_product.product_quantity,
                        product_price=price,
                    )
                    order_product.save()

                serializer = self.get_serializer(
                    instance=order
                )  # populating serializer with created object details
                body = serializer.data
                status_code = 201

                logger.info(
                    f"New order created. user_id: {user.pk}, order_id: {order.pk}"
                )

        except DatabaseError as e:
            body = {"detail": "Failed to create a new order"}
            status_code = 500

            logger.error(f"Failed to create a new order. error: {e}")

        # removing all items from cart
        cart.products.clear()

        return Response(data=body, status=status_code)
