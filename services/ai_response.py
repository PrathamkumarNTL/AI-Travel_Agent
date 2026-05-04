def generate_response(data):
    city = data["city"]
    days = data["days"]
    weather = data["weather"]
    places = ", ".join(data["places"])
    restaurants = ", ".join(data["restaurants"])
    cost = data["cost"]["total"]
    distance = data["route"]["distance_km"]

    response = f"""
    🌍 Trip Plan for {city} ({days} days)

    🌦 Weather: {weather}

    📍 Top Places:
    {places}

    🍽 Restaurants:
    {restaurants}

    🚗 Travel Distance: {distance} km

    💰 Estimated Cost: ₹{cost}

    👉 Enjoy your trip! 🎉
    """

    return response