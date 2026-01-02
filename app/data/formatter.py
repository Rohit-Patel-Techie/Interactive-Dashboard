import pandas as pd

def weather_data_to_dataframe(processed_data : dict) -> pd.DataFrame : 
    return pd.DataFrame([processed_data])