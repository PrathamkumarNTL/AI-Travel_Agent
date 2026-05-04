from services.weather import get_weather
from services.osm_places import get_places_osm, get_restaurants_osm
from services.cost import estimate_cost

def generate_plan(parsed):
    city = parsed["city"]
    days = parsed["days"]
    budget = parsed["budget"]

    weather = get_weather(city)
    places = get_places_osm(city)
    restaurants = get_restaurants_osm(city)
    cost = estimate_cost(days)

    # Budget filter logic
    within_budget = True
    if budget and cost["total"] > budget:
        within_budget = False

    return {
        "summary": f"{days}-day trip to {city}",
        "weather": weather,
        "places": places,
        "food": restaurants,
        "cost": cost,
        "budget_ok": within_budget
    }