from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'email']

class EmailCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)
