# 3rd party library imports
from rest_framework import serializers

# Local imports
from .models import Product
from utils.product import fetch_price


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    def get_price(self, obj) -> int:
        if hasattr(obj, 'price'):
            return obj.price

        price = fetch_price()
        return price * int(obj.weight)

    class Meta:
        model = Product
        fields = '__all__'
