""" Application Entry Point.
    Coordinates API calls and application flow. 
"""

from api.client import get_weather_by_city
from data_processing.weather_data_processor import extract_weather_info
from data.formatter import weather_data_to_dataframe
import pandas as pd
from datetime import datetime
import os
from visualization.weather_plots import get_weather_data_from_main

#Main Execution Function
#Get API Data
def run() -> None : 
    city = "jammu"

    try : 
        weather_data = get_weather_by_city(city)

        processed_data = extract_weather_info(weather_data)
        weather_dataframe = weather_data_to_dataframe(processed_data)
        weather_dataframe_formatter(weather_dataframe)

    except Exception as error:
        print(f"Error : {error}")

#Format Data in Datafram 
def weather_dataframe_formatter(data):
    #Append Header or Not
    file_path = "app/data/weather.csv"
    write_header = not os.path.exists(file_path)    

    #Add timestamp
    data["timestamp"] = datetime.now()

    #Making a new File CSV
    data.to_csv("app/data/weather.csv", mode = "a", header = write_header , index = False)

    #Sending a Data for visualization
    csv_data = pd.read_csv("app/data/weather.csv")
    get_weather_data_from_main(csv_data)

if __name__ == "__main__" :
    run()