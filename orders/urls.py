from .views import OrderViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'', OrderViewSet, basename='Order')

urlpatterns =[

] + router.urls