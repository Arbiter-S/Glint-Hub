# 3rd party library imports
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError

# Local imports
from orders.models import Order, OrderProduct
from products.models import Product


class ProductSummarySerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'picture']
        read_only_fields = ['id', 'name', 'picture']

class OrderProductSerializer(ModelSerializer):
    product = ProductSummarySerializer(read_only=True)

    class Meta:
        model = OrderProduct
        fields = ['product', 'product_quantity', 'product_price']


class OrderRetrieveSerializer(ModelSerializer):
    items = OrderProductSerializer(many=True, read_only=True, source='orderproduct_set')
    class Meta:
        model = Order
        fields = ['id','items', 'total_price', 'status', 'address', 'note', 'tracking_number']
        read_only_fields = ['id', 'total_price', 'status', 'tracking_number']

    def validate(self, attrs):
        request = self.context['request']
        if request.method == 'POST':
            user = request.user
            if not user.cart.products.all().exists():
                raise ValidationError('User has no products in their cart')
        elif request.method == 'PATCH':
            if self.instance.status not in ['pending', 'processing']:
                raise ValidationError("User can't change order info after it's been shipped or canceled")

        return attrs

class OrderListSerializer(ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'total_price', 'status', 'tracking_number']
        read_only_fields = ['id', 'total_price', 'status', 'tracking_number']
