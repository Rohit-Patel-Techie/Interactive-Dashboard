from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "weather_forecast_3hour.csv"

# Saving data to CSV File
def save_3hour_forecast_to_csv(forecast_data: list):
    df = pd.DataFrame(forecast_data)

    write_header = not DATA_PATH.exists()

    df.to_csv(
        DATA_PATH,
        mode="a",
        header=write_header,
        index=False
    )

    return df