import re

def parse_user_input(text):
    text = text.lower()

    # extract days
    days_match = re.search(r'(\d+)\s*day', text)
    days = int(days_match.group(1)) if days_match else 2

    # extract budget
    budget_match = re.search(r'(\d+)\s*(k|thousand)', text)
    if budget_match:
        budget = int(budget_match.group(1)) * 1000
    else:
        budget = None

    # extract city (simple approach)
    cities = ["goa", "delhi", "mumbai", "bangalore"]
    city = next((c.capitalize() for c in cities if c in text), "Goa")

    return {
        "city": city,
        "days": days,
        "budget": budget
    }