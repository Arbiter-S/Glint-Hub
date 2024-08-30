# 3rd party library imports
from django.db.models import Sum
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

# Local imports
from orders.models import Order
from orders.serializers import OrderSerializer
from products.utils import add_product_field


class OrderCreateView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # setting the fields
        user = self.request.user
        serializer.validated_data['user'] = user

        products = user.cart.products.all()
        serializer.validated_data['products'] = products

        total_price = add_product_field(queryset=products).aggregate(total_price=Sum('price'))['total_price']
        serializer.validated_data['total_price'] = total_price

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)