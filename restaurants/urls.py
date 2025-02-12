from django.urls import path
from restaurants.views import (
    RestaurantListCreateView,
    RestaurantRetrieveUpdateDestroyView,
    CategoryListCreateView,
    CategoryRetrieveUpdateDestroyView,
    MenuItemListCreateView,
    MenuItemRetrieveUpdateDestroyView,
)

urlpatterns = [
    path(
        "restaurants/",
        RestaurantListCreateView.as_view(),
        name="restaurant-list-create",
    ),
    path(
        "restaurants/<int:pk>/",
        RestaurantRetrieveUpdateDestroyView.as_view(),
        name="restaurant-detail",
    ),
    path("categories/", CategoryListCreateView.as_view(), name="category-list-create"),
    path(
        "categories/<int:pk>/",
        CategoryRetrieveUpdateDestroyView.as_view(),
        name="category-detail",
    ),
    path("menu-items/", MenuItemListCreateView.as_view(), name="menu-item-list-create"),
    path(
        "menu-items/<int:pk>/",
        MenuItemRetrieveUpdateDestroyView.as_view(),
        name="menu-item-detail",
    ),
]
