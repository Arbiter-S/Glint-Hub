from rest_framework.serializers import ModelSerializer
from orders.models import Order


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'total_price', 'status']
        read_only_fields = ['id', 'total_price', 'status']