# Making a Huge Weather data to Dashboard specified fields.

def extract_weather_info(raw_data : dict) -> dict : 
    return{
        "city" : raw_data.get("name"),
        "temperature" : raw_data.get("main" , {}).get("temp"),
        "humidity" : raw_data.get("main" , {}).get("humidity"),
        "condition" : raw_data.get("weather" , [{}])[0].get("description")

    }