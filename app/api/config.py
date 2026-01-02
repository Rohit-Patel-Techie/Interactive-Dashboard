""" API configuration setting for the weather Data
    This files contain only constants and configuration value.
"""

BASE_URL = "https://api.openweathermap.org/data/2.5"

WEATHER_ENDPOINT = "/weather"

DEFAULT_PARAMS= {
    "units" : "metric"
}

REQUEST_TIMEOUT =  5 # 5 Seconds


