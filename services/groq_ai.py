import requests
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

# -------------------------------
# 🔹 EXTRACT CITY & DAYS
# -------------------------------
def extract_trip_details(user_input):

    prompt = f"""
    Extract travel details from this sentence.

    Input: "{user_input}"

    Return ONLY JSON:
    {{
        "city": string or null,
        "days": number or null
    }}

    Do NOT assume values.
    If not present, return null.
    """

    body = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(URL, headers=HEADERS, json=body)
    result = response.json()

    if "choices" not in result:
        return {"city": None, "days": None}

    text = result["choices"][0]["message"]["content"]

    match = re.search(r'\{.*\}', text, re.DOTALL)

    if not match:
        return {"city": None, "days": None}

    try:
        return json.loads(match.group())
    except:
        return {"city": None, "days": None}


# -------------------------------
# 🔹 GENERATE FULL ITINERARY
# -------------------------------
def generate_itinerary(data):

    prompt = f"""
    You are an expert travel planner.

    City: {data['city']}
    Days: {data['days']}
    Weather: {data['weather']}

    Generate a COMPLETE travel guide including:

    1. 💰 Total Trip Cost
    2. 🌦 Weather during trip
    3. 🗺 Travel route
    4. 🏨 Hotels
    5. 🍽 Restaurants
    6. 🎉 Festivals / temples
    7. 🍛 Famous food
    8. 🚗 Transport options
    9. 🎧 Party places
    10. 📅 Day-wise itinerary

    Make it structured and practical.
    """

    body = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(URL, headers=HEADERS, json=body)
    result = response.json()

    if "choices" in result:
        return result["choices"][0]["message"]["content"]
    else:
        return f"AI Error: {result}"