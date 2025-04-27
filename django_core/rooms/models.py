from django.db import models
from rooms.constants import NAME_MAX_LENGTH


class Room(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH, verbose_name="Название комнаты")
    price_per_day = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="Цена за сутки"
    )
    capacity = models.PositiveSmallIntegerField(verbose_name="Количество мест")

    objects = models.Manager()

    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"


class Reservation(models.Model):
    room = models.ForeignKey(
        to="rooms.Room",
        on_delete=models.CASCADE,
        verbose_name="Зарезервированная комната",
    )
    user = models.ForeignKey(
        to="users.User", on_delete=models.CASCADE, verbose_name="Гость"
    )
    start_date = models.DateTimeField(verbose_name="Дата заезда")
    end_date = models.DateTimeField(verbose_name="Дата выезда")
