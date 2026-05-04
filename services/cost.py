def estimate_cost(days):
    hotel_per_day = 3000
    food_per_day = 1000
    travel = 5000

    total = (hotel_per_day + food_per_day) * days + travel

    return {
        "hotel": hotel_per_day * days,
        "food": food_per_day * days,
        "travel": travel,
        "total": total
    }