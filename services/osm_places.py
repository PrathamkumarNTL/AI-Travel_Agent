import requests

def safe_json(response):
    try:
        return response.json()
    except:
        print("❌ Bad response from OSM:")
        print(response.text[:200])
        return None


def get_places_osm(city):
    url = "https://overpass-api.de/api/interpreter"

    query = f"""
    [out:json];
    area["name"="{city}"]["boundary"="administrative"]->.searchArea;
    (
      node["tourism"="attraction"](area.searchArea);
    );
    out body;
    """

    try:
        response = requests.get(url, params={"data": query}, timeout=8)

        if response.status_code != 200:
            return ["Places API error"]

        data = safe_json(response)
        if not data:
            return ["No places data"]

        places = [
            el.get("tags", {}).get("name")
            for el in data.get("elements", [])[:5]
            if el.get("tags", {}).get("name")
        ]

        return places if places else ["No attractions found"]

    except Exception as e:
        print("ERROR:", e)
        return ["OSM failed"]


def get_restaurants_osm(city):
    url = "https://overpass-api.de/api/interpreter"

    query = f"""
    [out:json];
    area["name"="{city}"]["boundary"="administrative"]->.searchArea;
    (
      node["amenity"="restaurant"](area.searchArea);
    );
    out body;
    """

    try:
        response = requests.get(url, params={"data": query}, timeout=8)

        if response.status_code != 200:
            return ["Restaurant API error"]

        data = safe_json(response)
        if not data:
            return ["No restaurant data"]

        restaurants = [
            el.get("tags", {}).get("name")
            for el in data.get("elements", [])[:5]
            if el.get("tags", {}).get("name")
        ]

        return restaurants if restaurants else ["No restaurants found"]

    except Exception as e:
        print("ERROR:", e)
        return ["OSM failed"]