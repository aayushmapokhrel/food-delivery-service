import requests
from django.conf import settings
from orders.models import Order
from .models import Payment

ESEWA_BASE_URL = "https://uat.esewa.com.np/epay/main"

def initiate_esewa_payment(order: Order):
    payment_url = f"{ESEWA_BASE_URL}?amt={order.total_price}&psc=0&pdc=0&txAmt=0&tAmt={order.total_price}&pid={order.id}&scd={settings.ESEWA_MERCHANT_CODE}&su={settings.ESEWA_SUCCESS_URL}&fu={settings.ESEWA_FAILURE_URL}"
    Payment.objects.create(order=order, payment_method="esewa", amount=order.total_price, status="pending")

    return payment_url

def verify_esewa_payment(order_id: int, transaction_id: str):
    order = Order.objects.get(id=order_id)
    payment = Payment.objects.get(order=order)

    verification_url = "https://uat.esewa.com.np/epay/transrec"
    data = {
        "amt": order.total_price,
        "scd": settings.ESEWA_MERCHANT_CODE,
        "rid": transaction_id,
        "pid": order.id
    }

    response = requests.post(verification_url, data=data)
    if response.status_code == 200 and "Success" in response.text:
        order.payment_status = "paid"
        payment.status = "completed"
        order.esewa_transaction_id = transaction_id
    else:
        order.payment_status = "failed"
        payment.status = "failed"

    order.save()
    payment.save()
    return order.payment_status
