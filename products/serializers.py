# 3rd party library imports
from rest_framework import serializers

# Local imports
from .models import Product
from carts.models import Cart


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.IntegerField(source='total_price')

    class Meta:
        model = Product
        fields = '__all__'


class ProductAddCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart.products.through
        fields = ['product', ]
