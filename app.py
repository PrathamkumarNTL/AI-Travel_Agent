from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import sqlite3

from db import init_db
from services.weather import get_weather
from services.groq_ai import generate_itinerary,extract_trip_details

load_dotenv()

app = Flask(__name__)

init_db()

# ---------- HOME ----------
@app.route("/")
def home():
    return render_template("index.html")



@app.route("/chat", methods=["POST"])
def chat():
    user_text = request.json.get("message")

    if not user_text:
        return jsonify({"error": "Empty input"})

    parsed = extract_trip_details(user_text)

    city = parsed.get("city")
    days = parsed.get("days")

    if not city:
        return jsonify({"error": "Please mention a destination city."})

    if not days:
        return jsonify({"error": "Please mention number of days."})

    weather = get_weather(city)

    data = {
        "city": city,
        "days": days,
        "weather": weather
    }

    itinerary = generate_itinerary(data)

    return jsonify({
        "city": city,
        "days": days,
        "itinerary": itinerary
    })

# ---------- ADD EXPENSE ----------
@app.route("/add_expense", methods=["POST"])
def add_expense():
    data = request.json

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO expenses (purpose, person, amount) VALUES (?, ?, ?)",
        (data["purpose"], data["person"], data["amount"])
    )

    conn.commit()
    conn.close()

    return jsonify({"msg": "Expense added"})


# ---------- GET EXPENSES ----------
@app.route("/get_expenses", methods=["GET"])
def get_expenses():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT purpose, person, amount FROM expenses")
    rows = cursor.fetchall()

    expenses = [
        {"purpose": r[0], "person": r[1], "amount": r[2]} for r in rows
    ]

    total = sum(r[2] for r in rows)

    return jsonify({
        "expenses": expenses,
        "total": total
    })


if __name__ == "__main__":
    app.run(debug=True)