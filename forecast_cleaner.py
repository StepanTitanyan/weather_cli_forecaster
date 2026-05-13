import pandas as pd
from api import get_forecast_weather

def output_forecast_ready(df):
    df["date"] = df["date_time"].dt.date

    daily_summary = df.groupby("date").agg(
    min_temp=("temperature", "min"),
    max_temp=("temperature", "max"),
    avg_temp=("temperature", "mean"),
    avg_feels_like=("feels_like", "mean"),
    avg_humidity=("humidity", "mean"),
    avg_pressure=("pressure", "mean"),
    avg_cloudiness=("cloudiness", "mean"),
    avg_visibility=("visibility", "mean"),
    avg_wind_speed=("wind_speed", "mean"),
    max_wind_speed=("wind_speed", "max"),
    max_rain_probability=("rain_probability", "max"),
    total_rain_3h=("rain_3h", "sum")).reset_index()

    daily_condition = (df.groupby("date")["description"].agg(lambda x: x.value_counts().idxmax()))
    daily_icon = (df.groupby("date")["icon"].agg(lambda x: x.value_counts().idxmax()))
    daily_icon = daily_icon.str[0:2]

    daily_summary = daily_summary.merge(daily_icon, on="date")
    daily_summary = daily_summary.merge(daily_condition, on = "date")

    daily_summary["max_rain_probability"] = daily_summary["max_rain_probability"]*100
    daily_summary["rain_warning"] = daily_summary["max_rain_probability"].apply(lambda x: "Rain likely" if x >= 50 else "Low rain chance")
    daily_summary["wind_warning"] = daily_summary["max_wind_speed"].apply(lambda x: "Windy" if x >= 7 else "Normal wind")

    return daily_summary.to_dict(orient="records")

