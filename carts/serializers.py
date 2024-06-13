# 3rd party imports
from rest_framework import serializers

# local imports
from .models import Cart


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
