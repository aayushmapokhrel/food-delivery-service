from rest_framework import serializers
from restaurants.models import Restaurant, MenuItem, Category


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ["id", "owner", "name", "description", "address", "phone", "image"]
        read_only_fields = ["owner"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "restaurant", "name"]
        read_only_fields = ["restaurant"]


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = [
            "id",
            "restaurant",
            "category",
            "name",
            "description",
            "price",
            "image",
            "available",
        ]
        read_only_fields = ["restaurant"]
