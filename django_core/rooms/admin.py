from django.contrib import admin
from rooms.models import Reservation, Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price_per_day", "capacity")
    search_fields = ("name",)
    list_filter = ("capacity",)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "room", "start_date", "end_date")
    search_fields = ("user", "room")
