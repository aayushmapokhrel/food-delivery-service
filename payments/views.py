from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from orders.models import Order
from payments.models import Payment
from payments.services import initiate_esewa_payment, verify_esewa_payment


class InitiateEsewaPaymentView(APIView):

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)

        if order.payment_method != "esewa":
            return Response(
                {"error": "Invalid payment method"}, status=status.HTTP_400_BAD_REQUEST
            )

        payment_url = initiate_esewa_payment(order)
        return Response({"payment_url": payment_url}, status=status.HTTP_200_OK)


class VerifyEsewaPaymentView(APIView):

    def post(self, request, order_id):
        transaction_id = request.data.get("transaction_id")
        if not transaction_id:
            return Response(
                {"error": "Transaction ID required"}, status=status.HTTP_400_BAD_REQUEST
            )

        status = verify_esewa_payment(order_id, transaction_id)
        return Response({"payment_status": status}, status=status.HTTP_200_OK)


class CashOnDeliveryPaymentView(APIView):

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)

        if order.payment_method != "cod":
            return Response(
                {"error": "Invalid payment method"}, status=status.HTTP_400_BAD_REQUEST
            )

        order.payment_status = "paid"
        order.save()

        Payment.objects.create(
            order=order,
            payment_method="cod",
            amount=order.total_price,
            status="completed",
        )

        return Response(
            {
                "message": "Cash on Delivery confirmed",
                "payment_status": order.payment_status,
            },
            status=status.HTTP_200_OK,
        )
