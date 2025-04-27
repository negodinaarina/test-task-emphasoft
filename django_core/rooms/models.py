from django.db import models
from rooms.constants import NAME_MAX_LENGTH


class Room(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH, verbose_name="Room name")
    price_per_day = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="Price per day"
    )
    capacity = models.PositiveSmallIntegerField(verbose_name="Guest capacity")

    objects = models.Manager()

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"


class Reservation(models.Model):
    room = models.ForeignKey(
        to="rooms.Room",
        on_delete=models.CASCADE,
        verbose_name="reserved room",
    )
    user = models.ForeignKey(
        to="users.User", on_delete=models.CASCADE, verbose_name="Guest"
    )
    start_date = models.DateTimeField(verbose_name="Reservation start date")
    end_date = models.DateTimeField(verbose_name="Reservation end date")
    objects = models.Manager()

    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"
