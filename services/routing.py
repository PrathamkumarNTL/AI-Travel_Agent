import requests

def get_route(start, end):
    url = f"http://router.project-osrm.org/route/v1/driving/{start};{end}?overview=false"

    response = requests.get(url)
    data = response.json()

    if "routes" not in data:
        return "Route not found"

    route = data["routes"][0]

    return {
        "distance_km": round(route["distance"] / 1000, 2),
        "duration_min": round(route["duration"] / 60, 2)
    }