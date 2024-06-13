# 3rd party imports
from django.urls import path

# local imports
from .views import CartView


urlpatterns = [
    path('', CartView.as_view(), name='Cart')
]
