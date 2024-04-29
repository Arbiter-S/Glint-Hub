from django.urls import path, include
from .views import ProductListView

urlpatterns = [
    path('all/', ProductListView.as_view(), name='ProductList'),

]