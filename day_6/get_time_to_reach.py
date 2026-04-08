import sys
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

if not API_KEY: 
    print("Error: API key not found in .env file")
    sys.exit(1)


def get_travel_time(origin, destination):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    
    params = {
        "origins": origin,
        "destinations": destination,
        "key": API_KEY,
        "mode": "driving"
    }

    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print("Error: Unable to fetch data from API")
        sys.exit(1)

    data = response.json()

    try:
        duration_seconds = data["rows"][0]["elements"][0]["duration"]["value"]
        minutes = duration_seconds // 60
        return f"{minutes} Minutes"
    except (KeyError, IndexError):
        print("Error: Invalid response from API")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage: python get_time_to_reach.py "SOURCE" "DESTINATION"')
        sys.exit(1)

    source = sys.argv[1]
    destination = sys.argv[2]

    time = get_travel_time(source, destination)
    print(time)