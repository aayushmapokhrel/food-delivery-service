from django.urls import path
from payments.views import (
    InitiateEsewaPaymentView,
    VerifyEsewaPaymentView,
    CashOnDeliveryPaymentView,
)

urlpatterns = [
    path(
        "esewa/initiate/<int:order_id>/",
        InitiateEsewaPaymentView.as_view(),
        name="esewa-initiate",
    ),
    path(
        "esewa/verify/<int:order_id>/",
        VerifyEsewaPaymentView.as_view(),
        name="esewa-verify",
    ),
    path("cod/<int:order_id>/", CashOnDeliveryPaymentView.as_view(), name="cod"),
]
