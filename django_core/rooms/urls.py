from django.urls import path
from rooms.views import (
    AvailableRoomsAPIView,
    ReservationsDeleteAPIView,
    ReservationsGetAPIView,
)

urlpatterns = [
    path("", AvailableRoomsAPIView.as_view(), name="get rooms for reservation"),
    path("reservations/", ReservationsGetAPIView.as_view(), name="get and create reservations"),
    path(
        "reservations/<int:pk>",
        ReservationsDeleteAPIView.as_view(),
        name="delete reservation",
    ),
]
