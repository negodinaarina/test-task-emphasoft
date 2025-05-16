from rest_framework.routers import DefaultRouter
from rooms.views import RoomViewSet, ReservationViewSet

router = DefaultRouter()
router.register(r"rooms/available", RoomViewSet, basename="available-rooms")
router.register(r"reservations", ReservationViewSet, basename="reservations")

urlpatterns = router.urls
