from rest_framework import serializers
from rooms.models import Reservation, Room


class RoomRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("id", "name", "capacity", "price_per_day")


class ReservationRetrieveSerializer(serializers.ModelSerializer):
    room = RoomRetrieveSerializer()

    class Meta:
        model = Reservation
        fields = ("id", "start_date", "end_date", "room", "user")


class ReservationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ("start_date", "end_date", "room")
