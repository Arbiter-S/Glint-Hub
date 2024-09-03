# 3rd party imports
from django.urls import path

# local imports
from .views import CartViewSet


urlpatterns = [
    path('', CartViewSet.as_view({'get': 'retrieve', 'post': 'create'}), name='CartRetrieve'),
    path('<int:product_id>', CartViewSet.as_view({'delete': 'destroy'}), name='CartDestroy'),
]
