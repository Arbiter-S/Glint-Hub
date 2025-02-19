# 3rd party imports
# local imports
from .models import Cart, CartProduct
from products.models import Product
from products.serializers import ProductSerializer
from rest_framework import serializers


def validate_product_quantity(self, value):
    if value < 1:
        raise serializers.ValidationError("Quantity should be at least 1")

    product_id = self.initial_data["product_id"]
    product_instance = Product.objects.get(pk=product_id)
    if product_instance.in_stock is not None and product_instance.in_stock < value:
        raise serializers.ValidationError(
            f"Only {product_instance.in_stock} units available"
        )
    return value


class ProductCartSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    product = ProductSerializer(read_only=True)
    product_quantity = serializers.IntegerField()
    # TODO: See if it's possible to handle price like the approach used in products endpoint

    class Meta:
        model = CartProduct
        fields = ["product_id", "product_quantity", "product"]

    def validate_product_quantity(self, value):
        return validate_product_quantity(self, value)


class CartRetrieveSerializer(serializers.ModelSerializer):
    items = ProductCartSerializer(many=True, read_only=True, source="cartproduct_set")

    class Meta:
        model = Cart
        fields = ["items"]


class CartUpdateSerializer(serializers.ModelSerializer):
    product_quantity = serializers.IntegerField(min_value=1, required=True)

    class Meta:
        model = CartProduct
        fields = ["product_quantity"]

    def validate_product_quantity(self, value):
        return validate_product_quantity(self, value)
