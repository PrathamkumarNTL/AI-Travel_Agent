def get_places(city):
    data = {
        "Goa":["Baga Beach", "Anjuna Beach", "Fort Aguada"],
        "Delhi":["India Gate", "Red Fort", "Qutub Minar"]
    }

    return data.get(city,["No data available"])

def get_hotels(city):
    data ={
        "Goa": ["Taj Resort", "Beach Paradise Hotel"],
        "Delhi": ["The Leela Palace", "ITC Maurya"]
    }

    return data.get(city,["No hotels found"])