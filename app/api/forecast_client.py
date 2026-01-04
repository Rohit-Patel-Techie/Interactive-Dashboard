import requests
from .config import (BASE_URL, REQUEST_TIMEOUT)
from .client import Main_API

#Extract API from client.py
API_KEY = Main_API()

# Fetch 5-day weather forecast using City
def get_5_day_forecast(city : str) -> dict:
   
    url = f"{BASE_URL}/forecast"
    params = {
        "q" : city,
        "units": "metric",
        "appid": API_KEY,
    }
    response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.json()

