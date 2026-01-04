#Extracting Icon from openweather url
def get_weather_icon_url(icon_code):
    return f"https://openweathermap.org/img/wn/{icon_code}@2x.png"