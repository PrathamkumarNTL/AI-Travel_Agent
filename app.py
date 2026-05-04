from flask import Flask, request, jsonify, render_template, redirect, session
import sqlite3

from db import init_db

from services.weather import get_weather
from services.cost import estimate_cost
from services.osm_places import get_places_osm, get_restaurants_osm
from services.routing import get_route
from services.ai_parser import parse_user_input
from services.ai_response import generate_response

app = Flask(__name__)
app.secret_key = "secret123"

init_db()

# ---------- AUTH ----------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()

        if user:
            session["user_id"] = user[0]
            return redirect("/")
        else:
            return "Invalid credentials"

    return render_template("login.html")


@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
    except:
        return "User already exists"

    return redirect("/login")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------- HOME ----------

@app.route("/")
def home():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("index.html")

# ---------- AI CHAT ----------

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

    return jsonify({"ai_text": ai_text})

# ---------- EXPENSES ----------

@app.route("/add_expense", methods=["POST"])
def add_expense():
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"})

    data = request.json
    user_id = session["user_id"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO expenses (user_id, name, amount) VALUES (?, ?, ?)",
        (user_id, data["name"], data["amount"])
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Expense added"})


@app.route("/get_expenses", methods=["GET"])
def get_expenses():
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"})

    user_id = session["user_id"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name, amount FROM expenses WHERE user_id=?", (user_id,))
    rows = cursor.fetchall()

    expenses = [{"name": r[0], "amount": r[1]} for r in rows]
    total = sum(r[1] for r in rows)

    return jsonify({
        "expenses": expenses,
        "total": total
    })


if __name__ == "__main__":
    app.run(debug=True)