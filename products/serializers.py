# 3rd party library imports
from rest_framework import serializers

# Local imports
from .models import Product
from carts.models import Cart


class ProductSerializer(serializers.ModelSerializer):
    # price = serializers.IntegerField(source='price')

    class Meta:
        model = Product
        fields = '__all__'
