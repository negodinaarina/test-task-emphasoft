def make_room_filters(params):
    filters = {}

    min_price = params.get("min_price")
    max_price = params.get("max_price")
    min_capacity = params.get("min_capacity")
    max_capacity = params.get("max_capacity")

    if min_price is not None:
        filters["price_per_day__gte"] = min_price
    if max_price is not None:
        filters["price_per_day__lte"] = max_price
    if min_capacity is not None:
        filters["capacity__gte"] = min_capacity
    if max_capacity is not None:
        filters["capacity__lte"] = max_capacity

    return filters
