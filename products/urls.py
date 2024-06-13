from django.urls import path
from .views import ProductListView, ProductView

urlpatterns = [
    path('', ProductListView.as_view(), name='ProductList'),
    path('<int:pk>', ProductView.as_view(), name='ProductRetrieve')

]
