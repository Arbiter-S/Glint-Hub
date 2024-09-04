from django.urls import path
from rest_framework import routers
from .views import ProductViewSet

router = routers.SimpleRouter()
router.register(r'', ProductViewSet, basename='Product')

urlpatterns = [

] + router.urls
