from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.IntegerField(source='total_price')

    class Meta:
        model = Product
        fields = '__all__'
