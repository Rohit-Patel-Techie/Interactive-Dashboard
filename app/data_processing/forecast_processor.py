from datetime import datetime

#Extracting 3 Hour data from Raw Data
def extract_3hour_forecast(raw_forecast: dict) -> list:
    """
    Extract 3-hour forecast data from OpenWeather free API
    """
    forecast_list = []

    city_name = raw_forecast["city"]["name"]

    for item in raw_forecast.get("list", []):
        forecast_list.append({
            "city": city_name,
            "datetime": item["dt_txt"],
            "temperature": item["main"]["temp"],
            "feels_like": item["main"]["feels_like"],
            "temp_min": item["main"]["temp_min"],
            "temp_max": item["main"]["temp_max"],
            "humidity": item["main"]["humidity"],
            "pressure": item["main"]["pressure"],
            "weather": item["weather"][0]["description"],
            "wind_speed": item["wind"]["speed"]
        })

    return forecast_list