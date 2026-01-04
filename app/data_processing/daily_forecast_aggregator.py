import pandas as pd

# Converting 3 Hours data to Daily Basis
def convert_3hour_to_daily(df: pd.DataFrame) -> pd.DataFrame:
    # Safety check
    if isinstance(df, list):
        df = pd.DataFrame(df)

    df["date"] = pd.to_datetime(df["datetime"]).dt.date

    daily_df = df.groupby("date").agg({
        "temp_min": "min",
        "temp_max": "max",
        "humidity": "mean",
        "weather": lambda x: x.mode()[0]
    }).reset_index()

    return daily_df