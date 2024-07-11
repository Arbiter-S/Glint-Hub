# 3rd party imports
from django.urls import path

# local imports
from .views import CartView, CartAdd


urlpatterns = [
    path('', CartView.as_view(), name='CartRetrieve'),
    path('add/', CartAdd.as_view(), name='CartAdd')
]
