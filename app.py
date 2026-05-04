from flask import Flask, request, jsonify, render_template

from services.weather import get_weather
from services.cost import estimate_cost
from services.osm_places import get_places_osm, get_restaurants_osm
from services.routing import get_route
from services.ai_parser import parse_user_input
from services.ai_response import generate_response

app = Flask(__name__)

# In-memory expense storage
expenses = []

@app.route("/")
def home():
    return render_template("index.html")

# 🤖 AI Chat
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

    data = {
        "city": city,
        "days": days,
        "weather": weather,
        "places": places,
        "restaurants": restaurants,
        "cost": cost,
        "route": route
    }

    ai_text = generate_response(data)

    return jsonify({
        "raw": data,
        "ai_text": ai_text
    })

# 👥 Add expense
@app.route("/add_expense", methods=["POST"])
def add_expense():
    data = request.json
    expenses.append(data)
    return jsonify({"message": "Expense added"})

# 📊 Get expenses
@app.route("/get_expenses", methods=["GET"])
def get_expenses():
    total = sum(e["amount"] for e in expenses)
    return jsonify({
        "expenses": expenses,
        "total": total
    })


if __name__ == "__main__":
    app.run(debug=True)