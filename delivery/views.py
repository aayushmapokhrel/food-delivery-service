from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from delivery.models import Delivery, DeliveryPerson
from delivery.serializers import DeliverySerializer, DeliveryPersonSerializer
from django.utils.timezone import now
from orders.models import Order


class DeliveryPersonCreateView(generics.CreateAPIView):
    queryset = DeliveryPerson.objects.all()
    serializer_class = DeliveryPersonSerializer


class DeliveryPersonListView(generics.ListAPIView):
    queryset = DeliveryPerson.objects.all()
    serializer_class = DeliveryPersonSerializer


class DeliveryPersonDetailView(generics.RetrieveAPIView):
    queryset = DeliveryPerson.objects.all()
    serializer_class = DeliveryPersonSerializer


class DeliveryPersonUpdateView(generics.UpdateAPIView):
    queryset = DeliveryPerson.objects.all()
    serializer_class = DeliveryPersonSerializer


class DeliveryPersonDeleteView(generics.DestroyAPIView):
    queryset = DeliveryPerson.objects.all()
    serializer_class = DeliveryPersonSerializer


class CreateDeliveryView(generics.CreateAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer

    def create(self, request, *args, **kwargs):
        order_id = request.data.get("order")
        try:
            order_instance = Order.objects.get(id=order_id)
            delivery = Delivery.objects.create(
                order=order_instance, status="processing"
            )
            serializer = self.get_serializer(delivery)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND
            )


class AssignDeliveryPersonView(generics.UpdateAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        delivery = self.get_object()
        delivery_person_id = request.data.get("delivery_person_id")

        try:
            delivery_person = DeliveryPerson.objects.get(id=delivery_person_id)
            delivery.delivery_person = delivery_person
            delivery.status = "out_for_delivery"
            delivery.save()
            return Response(
                {"message": "Delivery person assigned!"},
                status=status.HTTP_200_OK
            )
        except DeliveryPerson.DoesNotExist:
            return Response(
                {"error": "Delivery person not found!"},
                status=status.HTTP_404_NOT_FOUND,
            )


class UpdateDeliveryStatusView(generics.UpdateAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        delivery = self.get_object()
        new_status = request.data.get("status")

        if new_status not in ["processing", "out_for_delivery", "delivered"]:
            return Response(
                {"error": "Invalid status!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_status == "delivered":
            delivery.delivered_at = now()

        delivery.status = new_status
        delivery.save()
        return Response(
            {"message": f"Order status updated to {new_status}!"},
            status=status.HTTP_200_OK,
        )


class RetrieveDeliveryView(generics.RetrieveAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated]


# NEW: List all deliveries
class ListAllDeliveriesView(generics.ListAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated]
