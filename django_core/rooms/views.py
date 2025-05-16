from datetime import datetime

from django.db.models import Q
from django.utils.dateparse import parse_datetime
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rooms.filters import RoomFilter
from rooms.models import Reservation, Room
from rooms.serializers import (
    ReservationCreateSerializer,
    ReservationRetrieveSerializer,
    RoomRetrieveSerializer,
)

@extend_schema_view(
    list=extend_schema(
        tags=["Rooms"],
        description="Get available rooms for the provided start and end dates",
        parameters=[
            OpenApiParameter(name="start_date", type=datetime, required=True),
            OpenApiParameter(name="end_date", type=datetime, required=True),
            OpenApiParameter(name="min_price", type=float, required=False),
            OpenApiParameter(name="max_price", type=float, required=False),
            OpenApiParameter(name="min_capacity", type=int, required=False),
            OpenApiParameter(name="max_capacity", type=int, required=False),
        ],
        responses=RoomRetrieveSerializer(many=True),
    )
)
class RoomViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = RoomRetrieveSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RoomFilter

    def get_queryset(self):
        start_date = parse_datetime(
            self.request.query_params.get("start_date")
        )
        end_date = parse_datetime(self.request.query_params.get("end_date"))

        if not start_date or not end_date or start_date >= end_date:
            return Room.objects.none()

        overlapping_reservations = Reservation.objects.filter(
            Q(start_date__lt=end_date) & Q(end_date__gt=start_date)
        ).values_list("room_id", flat=True)

        return Room.objects.exclude(id__in=overlapping_reservations)


@extend_schema_view(
    list=extend_schema(
        tags=["Reservations"],
        description="Get reservations (for authenticated user - "
        "user's reservations, for admin - all reservations)",
        responses=ReservationRetrieveSerializer(many=True),
    ),
    create=extend_schema(
        tags=["Reservations"],
        description="Create reservation for a room on given dates",
        request=ReservationCreateSerializer,
        responses=ReservationRetrieveSerializer,
    ),
    destroy=extend_schema(
        tags=["Reservations"],
        description="Delete reservation by ID",
    ),
)
class ReservationViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Reservation.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_admin:
            return Reservation.objects.all()
        return Reservation.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return ReservationCreateSerializer
        return ReservationRetrieveSerializer

    def perform_create(self, serializer):
        start_date = serializer.validated_data["start_date"]
        end_date = serializer.validated_data["end_date"]
        room = serializer.validated_data["room"]

        if start_date >= end_date:
            raise serializers.ValidationError(
                "Start date must be before end date."
            )

        overlapping = Reservation.objects.filter(
            room=room,
            start_date__lt=end_date,
            end_date__gt=start_date,
        ).exists()

        if overlapping:
            raise serializers.ValidationError(
                "Room is already reserved for the given dates."
            )

        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        reservation = self.get_object()
        if request.user.is_admin or reservation.user == request.user:
            reservation.delete()
            return Response(
                {"message": "Reservation successfully deleted."},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            {
                "error": "You do not have permission "
                "to delete this reservation."
            },
            status=status.HTTP_403_FORBIDDEN,
        )
