# 3rd party imports
# local imports
from .views import CartViewSet
from django.urls import path

urlpatterns = [
    path(
        "",
        CartViewSet.as_view({"get": "retrieve", "post": "create"}),
        name="CartRetrieve",
    ),
    path(
        "<int:product_id>",
        CartViewSet.as_view({"delete": "destroy", "patch": "update"}),
        name="CartUpdate",
    ),
]
