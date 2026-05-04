import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            return "Weather not available"

        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]

        return f"{city}: {weather}, {temp}°C"

    except:
        return "Weather fetch failed"