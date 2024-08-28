# 3rd party imports
from rest_framework import serializers

# local imports
from .models import Cart, CartProduct

class ProductCartSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = CartProduct
        fields = ['product_id', 'product_quantity']
        # TODO: find a way to add the price

class CartSerializer(serializers.ModelSerializer):
    items = ProductCartSerializer(many=True, read_only=True, source='cartproduct_set')

    class Meta:
        model = Cart
        fields = ['items']