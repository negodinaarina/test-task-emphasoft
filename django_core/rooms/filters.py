import django_filters
from rooms.models import Room


class RoomFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(
        field_name="price_per_day", lookup_expr="gte"
    )
    max_price = django_filters.NumberFilter(
        field_name="price_per_day", lookup_expr="lte"
    )
    min_capacity = django_filters.NumberFilter(field_name="capacity", lookup_expr="gte")
    max_capacity = django_filters.NumberFilter(field_name="capacity", lookup_expr="lte")

    class Meta:
        model = Room
        fields = ["min_price", "max_price", "min_capacity", "max_capacity"]
