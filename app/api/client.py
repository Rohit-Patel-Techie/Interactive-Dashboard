""" Client Module for interacting with the weather API.
    Handle API requests, responses,  and error management.
"""
import requests
from dotenv import load_dotenv
import os
from .config import (BASE_URL, WEATHER_ENDPOINT , DEFAULT_PARAMS , REQUEST_TIMEOUT)

load_dotenv()

API_KEY = os.getenv("API_KEY")

#Internal/Private function to Build Complete Base URL, Uses a Type hint function.
def _build_url(endpoint : str) -> str :
    return(f"{BASE_URL}{endpoint}")

#Function to Get Weather Data by City, Uses a Type Hint function.
def get_weather_by_city(city : str) -> dict : 
    
    #If city is empty
    if not city : 
        raise ValueError("City name cannot be empty")

    #Complete Parameter for weather data
    params = {
        **DEFAULT_PARAMS,
        "q" : city,
        "appid" : API_KEY
    }

    #Fetching Weather Data, Also handle Runtime error.
    try:
        response = requests.get(
            _build_url(WEATHER_ENDPOINT),
            params = params,
            timeout = REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as error : 
        raise RuntimeError(f"Weather API request failed : {error}")
    
def Main_API():
    return API_KEY




