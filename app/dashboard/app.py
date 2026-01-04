# PROJECT ROOT SETUP
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

# IMPORTS
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from app.api.client import get_weather_by_city
from app.api.forecast_client import get_5_day_forecast

from app.data_processing.weather_data_processor import extract_weather_info
from app.data_processing.forecast_processor import extract_3hour_forecast
from app.data_processing.daily_forecast_aggregator import convert_3hour_to_daily

from app.data.formatter import weather_data_to_dataframe
from app.data.forecast_formatter import save_3hour_forecast_to_csv
from app.utils.weather_icons import get_weather_icon_url

# PAGE CONFIG
st.set_page_config(
    page_title="🌦 Weather Dashboard",
    page_icon="🌤️",
    layout="wide"
)

st.title("🌦 Interactive Weather Dashboard")
st.caption("Real-Time, Historical & Forecast Weather Analysis")

# WEATHER THEME
def get_weather_theme(condition, temperature):
    c = condition.lower()
    if "clear" in c:
        return "#42A5F5"
    elif "cloud" in c:
        return "#90A4AE"
    elif "rain" in c:
        return "#1565C0"
    elif "storm" in c or "thunder" in c:
        return "#6A1B9A"
    elif temperature >= 35:
        return "#E53935"
    else:
        return "#FB8C00"

# LOAD HISTORICAL DATA
HIST_PATH = Path("app/data/weather.csv")

if HIST_PATH.exists():
    hist_df = pd.read_csv(HIST_PATH)
    hist_df["timestamp"] = pd.to_datetime(hist_df["timestamp"])
else:
    hist_df = pd.DataFrame(
        columns=["city", "temperature", "humidity", "condition", "timestamp"]
    )

# SIDEBAR
with st.sidebar:
    st.header("⚙ Controls")
    city_input = st.text_input("Enter City Name")
    cities = sorted(hist_df["city"].unique()) if not hist_df.empty else []
    selected_city = st.selectbox("Or select city", [""] + cities)
    hours = st.slider("Show last (hours)", 6, 72, 24)

city = city_input if city_input else selected_city

# MAIN LOGIC
if city:
    with st.spinner("Fetching weather data..."):

        # ---- Current Weather ----
        raw_current = get_weather_by_city(city)
        current = extract_weather_info(raw_current)
        format_data = weather_data_to_dataframe(current)

        # ---- Forecast ----
        raw_forecast = get_5_day_forecast(city)
        three_hour_list = extract_3hour_forecast(raw_forecast)
        save_3hour_forecast_to_csv(three_hour_list)

        three_hour_df = pd.DataFrame(three_hour_list)
        three_hour_df["datetime"] = pd.to_datetime(three_hour_df["datetime"])

        # Only next 48 hours → clean x-axis
        now = pd.Timestamp.now()
        three_hour_df_48 = three_hour_df[
            (three_hour_df["datetime"] >= now) &
            (three_hour_df["datetime"] <= now + pd.Timedelta(hours=48))
        ]

        five_day_df = convert_3hour_to_daily(three_hour_df)

    # THEME & ICON
    primary_color = get_weather_theme(
        current["condition"],
        current["temperature"]
    )
    icon_url = get_weather_icon_url(current["icon"])

    # WEATHER CARD (MODERN UI)
    st.markdown(
        f"""
        <style>
        .weather-card {{
            background: linear-gradient(135deg, {primary_color}, #1E88E5);
            border-radius: 18px;
            padding: 24px;
            color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
            margin-bottom: 20px;
        }}
        .weather-left h2 {{
            margin: 0;
            font-size: 18px;
            opacity: 0.9;
        }}
        .weather-left h1 {{
            font-size: 46px;
            margin: 6px 0;
        }}
        .weather-left p {{
            margin: 0;
            font-size: 16px;
            text-transform: capitalize;
        }}
        .weather-icon img {{
            width: 90px;
        }}
        </style>

        <div class="weather-card">
            <div class="weather-left">
                <h2>Current Weather</h2>
                <h1>{current["temperature"]}°C</h1>
                <p>💧 Humidity : <span>{current["humidity"]}°C</span></p>
                <p>{current["condition"]}</p>
            </div>
            <div class="weather-icon">
                <img src="{icon_url}">
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    # HISTORICAL DATA
    df_city = hist_df[hist_df["city"] == city]

    if not df_city.empty:
        cutoff = df_city["timestamp"].max() - pd.Timedelta(hours=hours)
        df_filt = df_city[df_city["timestamp"] >= cutoff]

        colA, colB = st.columns(2)

        # ---- Temperature Trend ----
        with colA:
            fig, ax = plt.subplots(figsize=(6, 3.5))
            ax.plot(df_filt["timestamp"], df_filt["temperature"],
                    color=primary_color, linewidth=2)

            ax.set_title("Temperature Trend")
            ax.set_ylabel("°C")

            ax.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=6))
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b\n%H:%M"))
            ax.grid(alpha=0.3)

            fig.tight_layout()
            st.pyplot(fig, use_container_width=True)

        # ---- Humidity Trend ----
        with colB:
            fig, ax = plt.subplots(figsize=(6, 3.5))
            ax.plot(df_filt["timestamp"], df_filt["humidity"],
                    color="#26A69A", linewidth=2)

            ax.set_title("Humidity Trend")
            ax.set_ylabel("%")

            ax.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=6))
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b\n%H:%M"))
            ax.grid(alpha=0.3)

            fig.tight_layout()
            st.pyplot(fig, use_container_width=True)

    # FORECAST SECTION
    st.subheader("📊 Forecast Overview")
    colC, colD = st.columns(2)

    # ---- 48-Hour Forecast ----
    with colC:
        fig, ax = plt.subplots(figsize=(6, 3.5))
        ax.plot(
            three_hour_df_48["datetime"],
            three_hour_df_48["temperature"],
            marker="o",
            linewidth=2,
            color=primary_color
        )

        ax.set_title("Next 48 Hours (3-Hour Interval)")
        ax.set_ylabel("°C")

        ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b\n%H:%M"))
        ax.grid(alpha=0.3)

        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)

    # ---- 5-Day Forecast ----
    with colD:
        fig, ax = plt.subplots(figsize=(6, 3.5))
        ax.plot(five_day_df["date"], five_day_df["temp_max"],
                label="Max", marker="o", color="#E53935")
        ax.plot(five_day_df["date"], five_day_df["temp_min"],
                label="Min", marker="o", color="#1E88E5")

        ax.set_title("5-Day Forecast")
        ax.set_ylabel("°C")
        ax.legend()
        ax.grid(alpha=0.3)

        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)

else:
    st.info("👈 Enter or select a city to view weather data")
