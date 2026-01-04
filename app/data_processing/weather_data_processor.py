# Extracting Current Weather Information from Raw Data
def extract_weather_info(raw_data : dict) -> dict : 
    return{
        "city" : raw_data.get("name"),
        "temperature" : raw_data.get("main" , {}).get("temp"),
        "humidity" : raw_data.get("main" , {}).get("humidity"),
        "condition" : raw_data.get("weather" , [{}])[0].get("description"),
        "icon": raw_data["weather"][0]["icon"], 

    }