from api import get_lat_lon_call, get_current_weather, get_forecast_weather, get_current_pollution
from forecast_cleaner import output_forecast_ready
from mapping import ICON_MAP
import re
from datetime import datetime, timedelta

def choose_location():
    while True:
        inputed_loc_name = input("Enter location: ")
        pattern = r'^[a-zA-Z\s]+$'
        is_valid = bool(re.fullmatch(pattern, inputed_loc_name))
        if is_valid:
            choices = get_lat_lon_call(inputed_loc_name)
            if isinstance(choices, dict) and choices.get("error"):
                print("Error:", choices.get("message"))
                continue
            if choices:
                print("Please clarify the location")
                for x, example in enumerate(choices):
                    print(f"{x + 1}: {example.get('name')} {example.get('state', '').strip()}, {example.get('country')}")
                
                while True:
                    choice = input("Choose: ")

                    if choice.isdigit():
                        choice = int(choice) - 1

                        if 0 <= choice < len(choices):
                            return choices[choice].get("lat"), choices[choice].get("lon")

                    print("-Please choose a valid entry-")
            else:
                return
        else:
            print("-Not a valid Location, Please try again-")


def choose_units():
        print("\nChoose temperature units:")
        print("1. Celsius")
        print("2. Fahrenheit")

        choice = input("Enter choice: ")

        if choice == "1":
            return "metric", "°C"
        elif choice == "2":
            return "imperial", "°F"
        else:
            print("Invalid choice. Using Celsius by default.")
            return "metric", "°C"
        
def show_menu():
    print("\n=== Weather Forecast CLI ===")
    print("||   1. Current Weather   ||")
    print("||   2. 5-Day Forecast    ||")
    print("||   3. Air Quality       ||")
    print("||   4. Full Report       ||")
    print("||   5. Change Location   ||")
    print("||   6. Change Units      ||")
    print("||   7. Exit              ||")
    print("=" * 28)

    while True:
        choice = input("Choose option: ")

        if choice.isdigit():
            choice = int(choice)

            if 1 <= choice <= 7:
                return choice

        print("-Not a valid option, Please try again-")

def print_box_line(text, width=35):
    print(f"|| {text:<{width}} ||")

def display_current_weather(cur_weather, unit_symbol):
    if cur_weather.get("error"):
        print("Error:", cur_weather.get("message"))
        return
    width = 35

    sunrise = (cur_weather.get("sunrise") + timedelta(hours=cur_weather.get("timezone"))).strftime("%H:%M")
    sunset = (cur_weather.get("sunset") + timedelta(hours=cur_weather.get("timezone"))).strftime("%H:%M")

    print("\n=== Current Weather ===")
    print("||" + "-" * (width + 2) + "||")
    print_box_line(f"📍 {cur_weather.get('city')}, {cur_weather.get('country')}", width)
    print_box_line(f"{ICON_MAP.get(cur_weather.get('icon'), "🌡️")}  {cur_weather.get('description')}", width)
    print("||" + "-" * (width + 2) + "||")
    print_box_line(f"Temperature: {cur_weather.get('temperature')}{unit_symbol}", width)
    print_box_line(f"Feels like: {cur_weather.get('feels_like')}{unit_symbol}", width)
    print_box_line(f"Humidity: {cur_weather.get('humidity')}%", width)
    print_box_line(f"Pressure: {cur_weather.get('pressure')} hPa", width)
    print_box_line(f"Wind speed: {cur_weather.get('wind_speed')} m/s", width)
    print_box_line(f"Cloudiness: {cur_weather.get('cloudiness')}%", width)
    print_box_line(f"Visibility: {cur_weather.get('visibility')} km", width)
    print_box_line(f"Sunrise: {sunrise} local time", width)
    print_box_line(f"Sunset: {sunset} local time", width)
    print("||" + "-" * (width + 2) + "||")
    print_box_line("-Fetched at-", width)
    print_box_line(datetime.now().strftime("%Y-%m-%d %H:%M"), width)
    print("=" * (width + 6))


def display_forecast(forecast_items, unit_symbol):
    if isinstance(forecast_items, dict) and forecast_items.get("error"):
        print("Error:", forecast_items.get("message"))
        return

    print("\n=== 5-Day Forecast ===" + "="*68)

    print("||" + "-" * 86 + "||")
    print(f"|| {'Date':<12} {'Condition':<22} {'Visibility':>5} {'Min':>7} {'Max':>9} {'Rain':>8} {'Wind':>9}  ||")
    print("||" + "-" * 86 + "||")

    for day in forecast_items:
        icon = ICON_MAP.get(day.get("icon") + "d", "🌡️")
        condition = f"{icon}  {day.get('description')}"
        visibility = f"{day.get('avg_visibility'):.1f} km"

        date = str(day.get("date"))
        min_temp = f"{day.get('min_temp'):.1f}{unit_symbol}"
        max_temp = f"{day.get('max_temp'):.1f}{unit_symbol}"
        rain = f"{day.get('max_rain_probability'):.0f}%"
        wind = f"{day.get('avg_wind_speed'):.1f} m/s"

        print(
            f"|| {date:<12} "
            f"{condition:<22} "
            f"{visibility:>6} "
            f"{min_temp:>10} "
            f"{max_temp:>10} "
            f"{rain:>7} "
            f"{wind:>10}  ||")

    print("||" + "-" * 86 + "||")
    print("=" * 90)

def display_temperature_chart(forecast_items, unit_symbol):
    if not forecast_items:
        print("No forecast data available.")
        return

    max_temp = max(day.get("max_temp") for day in forecast_items)
    min_temp = min(day.get("min_temp") for day in forecast_items)
    max_abs_temp = max(abs(day.get("max_temp")) for day in forecast_items)

    print("\n=== Temperature Trend ===")

    for day in forecast_items:
        date = str(day.get("date"))
        temp = day.get("max_temp")

        if max_abs_temp == 0:
            bar_length = 1
        else:
            bar_length = int((abs(temp) / max_abs_temp) * 30)

        bar_length = max(1, bar_length)
        if temp >= 0:
            bar = "❚" * bar_length
        else:
            bar = "❄" * bar_length

        print(f"|| {date} | {bar:<30} {temp:.1f}{unit_symbol}")

    print("=" * 55)
    print(f"\nLowest forecast temperature: {min_temp:.1f}{unit_symbol}")
    print(f"Highest forecast temperature: {max_temp:.1f}{unit_symbol}")

def display_air_pollution(air):
    if air.get("error"):
        print("Error:", air.get("message"))
        return

    width = 30

    print("\n====== Air Quality ======")
    print("||" + "-" * (width + 2) + "||")
    print_box_line(f"AQI: {air.get('aqi')} - {air.get('aqi_label')}", width)
    print("||" + "-" * (width + 2) + "||")
    print_box_line(f"CO: {air.get('co')} μg/m³", width)
    print_box_line(f"NO: {air.get('no')} μg/m³", width)
    print_box_line(f"NO2: {air.get('no2')} μg/m³", width)
    print_box_line(f"O3: {air.get('o3')} μg/m³", width)
    print_box_line(f"SO2: {air.get('so2')} μg/m³", width)
    print_box_line(f"PM2.5: {air.get('pm2_5')} μg/m³", width)
    print_box_line(f"PM10: {air.get('pm10')} μg/m³", width)
    print_box_line(f"NH3: {air.get('nh3')} μg/m³", width)
    print("||" + "-" * (width + 2) + "||")
    print("=" * (width + 6))

# z = get_current_weather(33.44, -94)
# y = output_forecast_ready(get_forecast_weather(33.44, -94))
# x = get_current_pollution(33.44, -94)

# display_current_weather(z, "°C")
# display_forecast(y, "°C")
# display_temperature_chart(y, "°C")
# display_air_pollution(x)

# print(show_menu())