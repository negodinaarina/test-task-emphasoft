from datetime import datetime

from django.db.models import Q
from django.utils.dateparse import parse_datetime
from django.utils.decorators import method_decorator
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rooms.models import Reservation, Room
from rooms.serializers import ReservationCreateSerializer, ReservationRetrieveSerializer, RoomRetrieveSerializer
from rooms.utils import make_room_filters


class AvailableRoomsAPIView(APIView):
    permission_classes = [AllowAny]

    @method_decorator(
        name="get",
        decorator=extend_schema(
            tags=["Rooms"],
            description="Get available rooms for the provided start and end dates",
            responses=RoomRetrieveSerializer(many=True),
            parameters=[
                OpenApiParameter(
                    name="start_date",
                    type=datetime,
                    description="Reservation start date",
                    required=True,
                ),
                OpenApiParameter(
                    name="end_date",
                    type=datetime,
                    description="Reservation end date",
                    required=True,
                ),
                OpenApiParameter(
                    name="min_price",
                    type=float,
                    description="Minimum price per day",
                    required=False,
                ),
                OpenApiParameter(
                    name="max_price",
                    type=float,
                    description="Maximum price per day",
                    required=False,
                ),
                OpenApiParameter(
                    name="min_capacity",
                    type=int,
                    description="Minimum room capacity",
                    required=False,
                ),
                OpenApiParameter(
                    name="max_capacity",
                    type=int,
                    description="Maximum room capacity",
                    required=False,
                ),
            ],
        ),
    )
    def get(self, request, *args, **kwargs):
        """
        Get available rooms on given dates
        """
        start_date = parse_datetime(str(request.query_params.get("start_date")))
        end_date = parse_datetime(str(request.query_params.get("end_date")))

        if not start_date or not end_date:
            return Response(
                {"error": "Incorrect date format"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if start_date >= end_date:
            return Response(
                {"error": "Start date must be before end date"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        overlapping_reservations = Reservation.objects.filter(
            Q(start_date__lt=end_date) & Q(end_date__gt=start_date)
        ).values_list("room_id", flat=True)

        available_rooms = Room.objects.exclude(id__in=overlapping_reservations)
        filters = make_room_filters(request.query_params)
        available_rooms = available_rooms.filter(**filters)

        serializer = RoomRetrieveSerializer(available_rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReservationsGetAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(
        name="get",
        decorator=extend_schema(
            tags=["Reservations"],
            description="Get reservations (for authenticated user - user's reservations, for admin - all reservations)",
            responses=ReservationRetrieveSerializer(many=True),
        ),
    )
    def get(self, request, *args, **kwargs):
        """
        Get user's reservations (all reservations for administrator)
        """
        if request.user.is_admin:
            reservations = Reservation.objects.all()
            serializer = ReservationRetrieveSerializer(reservations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            reservations = Reservation.objects.filter(user=request.user)
            serializer = ReservationRetrieveSerializer(reservations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(
        name="post",
        decorator=extend_schema(
            tags=["Reservations"],
            description="Create reservation for a room on given dates",
            responses=ReservationRetrieveSerializer(),
            request=ReservationCreateSerializer(),
        ),
    )
    def post(self, request, *args, **kwargs):
        """
        Create new reservation
        """
        start_date = parse_datetime(str(request.data.get("start_date")))
        end_date = parse_datetime(str(request.data.get("end_date")))
        room_id = request.data.get("room")

        if not start_date or not end_date or not room_id:
            return Response(
                {"error": "Incorrect request body"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if start_date >= end_date:
            return Response(
                {"error": "Start date must be before end date"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response(
                {"error": "Room does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        overlapping = Reservation.objects.filter(
            room=room,
            start_date__lt=end_date,
            end_date__gt=start_date,
        ).exists()

        if overlapping:
            return Response(
                {"error": "Room is already reserved for the given dates."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        reservation = Reservation.objects.create(
            room=room,
            user=request.user,
            start_date=start_date,
            end_date=end_date,
        )

        serializer = ReservationRetrieveSerializer(reservation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReservationsDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None

    @method_decorator(
        name="delete",
        decorator=extend_schema(
            tags=["Reservations"],
            description="Delete reservation",
        ),
    )
    def delete(self, request, pk, *args, **kwargs):
        """Delete reservation"""
        try:
            reservation = Reservation.objects.get(id=pk)
        except Reservation.DoesNotExist:
            return Response(
                {"error": "Reservation does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        if request.user.is_admin or request.user.id == reservation.user.id:
            reservation.delete()
            return Response(
                {"message": "Reservation successfully deleted."},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {"error": "You do not have permission to delete this reservation."},
                status=status.HTTP_403_FORBIDDEN,
            )
