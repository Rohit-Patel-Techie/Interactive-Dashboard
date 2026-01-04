import os
import pandas as pd
from datetime import datetime

# Converting Dictionary to DataFrame
def weather_data_to_dataframe(processed_data : dict) -> pd.DataFrame : 
    df = pd.DataFrame([processed_data])

    #Append Header or Not
    file_path = "app/data/weather.csv"
    write_header = not os.path.exists(file_path)    

    #Add timestamp
    df["timestamp"] = datetime.now()

    #Making a new File CSV
    df.to_csv("app/data/weather.csv", mode = "a", header = write_header , index = False)
    return df
