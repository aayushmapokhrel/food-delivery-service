from rest_framework import serializers
from delivery.models import Delivery, DeliveryPerson


class DeliveryPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryPerson
        fields = ["id", "user", "phone_number", "vehicle_number"]


class DeliverySerializer(serializers.ModelSerializer):
    delivery_person = DeliveryPersonSerializer(read_only=True)
    delivery_person_id = serializers.IntegerField(
        write_only=True,
        required=False
        )

    class Meta:
        model = Delivery
        fields = [
            "id",
            "order",
            "delivery_person",
            "delivery_person_id",
            "status",
            "created_at",
            "delivered_at",
        ]
        read_only_fields = ["created_at", "delivered_at"]

    def update(self, instance, validated_data):
        delivery_person_id = validated_data.pop("delivery_person_id", None)
        if delivery_person_id:
            instance.delivery_person_id = delivery_person_id
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance
