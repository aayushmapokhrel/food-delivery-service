from django.urls import path
from delivery.views import (
    AssignDeliveryPersonView,
    UpdateDeliveryStatusView,
    RetrieveDeliveryView,
    ListAllDeliveriesView,
    CreateDeliveryView,
    DeliveryPersonListView,
    DeliveryPersonCreateView,
    DeliveryPersonDetailView,
    DeliveryPersonUpdateView,
    DeliveryPersonDeleteView
)

urlpatterns = [
    path("create/", CreateDeliveryView.as_view(), name="create_delivery"),
    path(
        "assign/<int:pk>/",
        AssignDeliveryPersonView.as_view(),
        name="assign-delivery-person",
    ),
    path(
        "status/update/<int:pk>/",
        UpdateDeliveryStatusView.as_view(),
        name="update-delivery-status",
    ),
    path(
        "detail/<int:pk>/", RetrieveDeliveryView.as_view(), name="delivery-detail"
    ),
    path("list/", ListAllDeliveriesView.as_view(), name="list-all-deliveries"),
    path(
        "delivery-persons/",
        DeliveryPersonListView.as_view(),
        name="delivery_person_list",
    ),
    path(
        "delivery-persons/create/",
        DeliveryPersonCreateView.as_view(),
        name="delivery_person_create",
    ),
    path(
        "delivery-persons/<int:pk>/",DeliveryPersonDetailView.as_view(),
        name="delivery_person_detail",
    ),
    path(
        "delivery-persons/<int:pk>/update/",
        DeliveryPersonUpdateView.as_view(),
        name="delivery_person_update",
    ),
    path(
        "delivery-persons/<int:pk>/delete/",
        DeliveryPersonDeleteView.as_view(),
        name="delivery_person_delete",
    ),
]
