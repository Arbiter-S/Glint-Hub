from .views import PaymentInitiatorView, PaymentVerifierView
from django.urls import path

urlpatterns = [
    path(
        "initiate/<int:order_id>/",
        PaymentInitiatorView.as_view(),
        name="PaymentInitiator",
    ),
    path("verify/callback", PaymentVerifierView.as_view(), name="PaymentInitiator"),
]
