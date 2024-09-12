# 3rd party imports
from rest_framework import serializers

# local imports
from .models import Cart, CartProduct
from products.serializers import ProductSerializer

class ProductCartSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    product = ProductSerializer(read_only=True)
    # TODO: See if it's possible to handle price like the approach used in products endpoint

    class Meta:
        model = CartProduct
        fields = ['product_id', 'product_quantity', 'product']

class CartRetrieveSerializer(serializers.ModelSerializer):
    items = ProductCartSerializer(many=True, read_only=True, source='cartproduct_set')

    class Meta:
        model = Cart
        fields = ['items']

class CartUpdateSerializer(serializers.ModelSerializer):
    product_quantity = serializers.IntegerField(min_value=1, required=True)


    class Meta:
        model = CartProduct
        fields = ['product_quantity']
