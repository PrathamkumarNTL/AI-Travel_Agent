from flask import Flask, request, jsonify, render_template

from services.weather import get_weather
from services.cost import estimate_cost
from services.osm_places import get_places_osm, get_restaurants_osm
from services.routing import get_route
from services.ai_parser import parse_user_input

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_text = request.json.get("message")

    parsed = parse_user_input(user_text)

    city = parsed["city"]
    days = parsed["days"]

    weather = get_weather(city)
    places = get_places_osm(city)
    restaurants = get_restaurants_osm(city)
    cost = estimate_cost(days)

    route = get_route("77.5946,12.9716", "73.8567,15.2993")

    response = {
        "city": city,
        "days": days,
        "weather": weather,
        "places": places,
        "restaurants": restaurants,
        "cost": cost,
        "route": route
    }

    return jsonify(response)


# if __name__ == "__main__":
#     app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)