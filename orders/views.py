from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from orders.models import Order
from orders.serializers import OrderSerializer
from django.shortcuts import get_object_or_404
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderSerializer

    @action(detail=True, methods=["patch"])
    def update_status(self, request, pk=None):
        """
        Allows the restaurant to update the order status.
        """
        order = get_object_or_404(Order, pk=pk)
        new_status = request.data.get("status")

        if new_status not in ["Pending", "Processing", "Out for Delivery", "Delivered"]:
            return Response({"error": "Invalid status update"}, status=400)

        order.status = new_status
        order.save()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"order_{order.id}",
            {
                "type": "order_update",
                "message": json.dumps({"order_id": order.id, "status": order.status}),
            },
        )

        return Response({"message": "Order status updated successfully!"})
