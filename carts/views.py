# 3rd party library imports
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

# Local imports
from .models import Cart
from .serializers import CartSerializer


class CartView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_object(self):
        return Cart.objects.get(user=self.request.user)
