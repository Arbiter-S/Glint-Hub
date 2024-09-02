# 3rd party imports
from django.urls import path
from rest_framework import routers

# local imports
from .views import CartViewSet


urlpatterns = [
    path('', CartViewSet.as_view({'get': 'retrieve', 'post': 'create'}), name='CartRetrieve'),
]
