import requests
import json
import pandas as pd
from datetime import datetime, timezone as dt_timezone
from config import API_KEY
from mapping import AQI_LABELS
from cache import get_from_cache, save_to_cache


def get_lat_lon_call(loc_name:str):
    cache_key = f"geo_{loc_name}"
    cached_data = get_from_cache(cache_key)

    if cached_data is not None:
        resp_json = cached_data
    else:
        base_url = f"https://api.openweathermap.org/geo/1.0/direct?q={loc_name}&limit=5&appid={API_KEY}"
        response = requests.get(base_url, timeout = 20)
        resp_json = response.json()
        if response.status_code != 200:
            return {"error": True, "message": resp_json.get("message", "API request failed")}
        save_to_cache(cache_key, resp_json)

    locations = []

    for item in resp_json:
        location = {
            "name": item.get("name", "Unknown"),
            "country": item.get("country", "Unknown"),
            "state": item.get("state", ""),
            "lat": item.get("lat"),
            "lon": item.get("lon")}

        locations.append(location)

    return locations


def get_current_weather(lat:float, lon:float, units:str = "metric"):
    cache_key = f"current_{lat}_{lon}_{units}"
    cached_data = get_from_cache(cache_key)

    if cached_data is not None:
        resp_json = cached_data
    else:
        base_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units={units}&appid={API_KEY}"
        response = requests.get(base_url, timeout = 20)
        resp_json = response.json()
        if response.status_code != 200:
            return {"error": True, "message": resp_json.get("message", "API request failed")}
        save_to_cache(cache_key, resp_json)

    weather = resp_json.get("weather", [{}])[0]

    result = {
        "city": resp_json.get("name", "Unknown"),
        "country": resp_json.get("sys", {}).get("country", "Unknown"),
        "temperature": resp_json.get("main", {}).get("temp"),
        "feels_like": resp_json.get("main", {}).get("feels_like"),
        "temp_min": resp_json.get("main", {}).get("temp_min"),
        "temp_max": resp_json.get("main", {}).get("temp_max"),
        "humidity": resp_json.get("main", {}).get("humidity"),
        "pressure": resp_json.get("main", {}).get("pressure"),
        "weather_main": weather.get("main"),
        "description": weather.get("description"),
        "icon": weather.get("icon"),
        "wind_speed": resp_json.get("wind", {}).get("speed"),
        "wind_direction": resp_json.get("wind", {}).get("deg"),
        "cloudiness": resp_json.get("clouds", {}).get("all"),
        "visibility": round(resp_json.get("visibility")/1000,2) if resp_json.get("visibility") is not None else None,
        "sunrise": datetime.fromtimestamp(resp_json.get("sys", {}).get("sunrise"), tz=dt_timezone.utc),
        "sunset": datetime.fromtimestamp(resp_json.get("sys", {}).get("sunset"), tz=dt_timezone.utc),
        "timezone": resp_json.get("timezone")/3600 if resp_json.get("timezone") is not None else None}
    return result



def get_forecast_weather(lat:float, lon:float, units:str = "metric"):
    cache_key = f"forecast_{lat}_{lon}_{units}"
    cached_data = get_from_cache(cache_key)

    if cached_data is not None:
        resp_json = cached_data
    else:
        base_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units={units}&appid={API_KEY}"
        response = requests.get(base_url, timeout = 20)
        resp_json = response.json()
        if response.status_code != 200:
            return {"error": True, "message": resp_json.get("message", "API request failed")}
        save_to_cache(cache_key, resp_json)

    forecast_items = []

    for item in resp_json.get("list", []):
        weather = item.get("weather", [{}])[0]

        parsed_item = {
            "date_time": datetime.strptime(item.get("dt_txt"), "%Y-%m-%d %H:%M:%S"),
            "temperature": item.get("main", {}).get("temp"),
            "feels_like": item.get("main", {}).get("feels_like"),
            "humidity": item.get("main", {}).get("humidity"),
            "pressure": item.get("main", {}).get("pressure"),
            "weather_main": weather.get("main"),
            "description": weather.get("description"),
            "icon": weather.get("icon"),
            "cloudiness": item.get("clouds", {}).get("all"),
            "visibility": round(item.get("visibility")/ 1000, 2) if item.get("visibility") is not None else None,
            "wind_speed": item.get("wind", {}).get("speed"),
            "wind_direction": item.get("wind", {}).get("deg"),
            "rain_probability": item.get("pop", 0),
            "rain_3h": item.get("rain", {}).get("3h", 0)}

        forecast_items.append(parsed_item)

    return pd.DataFrame(forecast_items)


def get_current_pollution(lat:float, lon:float):
    cache_key = f"pollution_{lat}_{lon}"
    cached_data = get_from_cache(cache_key)

    if cached_data is not None:
        resp_json = cached_data
    else:
        base_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
        response = requests.get(base_url, timeout = 20)
        resp_json = response.json()
        if response.status_code != 200:
            return {"error": True, "message": resp_json.get("message", "API request failed")}
        save_to_cache(cache_key, resp_json)

    air_item = resp_json.get("list", [{}])[0]
    main = air_item.get("main", {})
    components = air_item.get("components", {})



    parsed = {
        "aqi": main.get("aqi"),
        "aqi_label": AQI_LABELS.get(main.get("aqi"), "Unknown"),
        "co": components.get("co"),
        "no": components.get("no"),
        "no2": components.get("no2"),
        "o3": components.get("o3"),
        "so2": components.get("so2"),
        "pm2_5": components.get("pm2_5"),
        "pm10": components.get("pm10"),
        "nh3": components.get("nh3"),
        "dt": datetime.fromtimestamp(air_item.get("dt"))}

    return parsed
