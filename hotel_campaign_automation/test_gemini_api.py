import requests
import json

BASE_URL = "http://localhost:8000"

def test_generate_campaign():
    url = f"{BASE_URL}/generate_campaign"
    payload = {
        "target_audience": "Families with young children",
        "hotel_info": "Beachfront resort with kids club and family-friendly activities",
        "campaign_type": "Summer vacation package"
    }
    response = requests.post(url, json=payload)
    print("Generate Campaign Response:")
    print(json.dumps(response.json(), indent=2))
    print("\n")

def test_optimize_timing():
    url = f"{BASE_URL}/optimize_timing"
    payload = {
        "occupancy_rate": 65,
        "current_month": "April",
        "historical_data": {
            "low_season": ["November", "December", "January"],
            "high_season": ["June", "July", "August"]
        },
        "upcoming_events": ["Local festival in May", "School holidays starting in June"]
    }
    response = requests.post(url, json=payload)
    print("Optimize Timing Response:")
    print(json.dumps(response.json(), indent=2))
    print("\n")

if __name__ == "__main__":
    test_generate_campaign()
    test_optimize_timing()
