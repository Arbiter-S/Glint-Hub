from .views import ProductViewSet
from django.urls import path
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r"", ProductViewSet, basename="Product")

urlpatterns = [] + router.urls
