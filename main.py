from api import get_current_weather, get_forecast_weather, get_current_pollution
from cli_visuals import choose_location, choose_units, show_menu, display_current_weather, display_forecast, display_temperature_chart, display_air_pollution
from forecast_cleaner import output_forecast_ready


def main():
    print("\n" + "="*37)
    print("||     🌤️  Weather Forecast CLI    ||")
    print("|| Current Weather • Forecast • AQI||")
    print("="*37)

    while True:
        loc = choose_location()
        if loc:
            lat, lon = loc[0], loc[1]
            units, unit_symbol = choose_units()
            break
            
        else:
                print("No such location found, please try again")
    while True:
        choice = show_menu()

        if choice == 1:
            current_weather = get_current_weather(lat, lon, units)
            display_current_weather(current_weather, unit_symbol)

        elif choice == 2:
            forecast_df = get_forecast_weather(lat, lon, units)

            if isinstance(forecast_df, dict) and forecast_df.get("error"):
                print("Error:", forecast_df.get("message"))
            else:
                forecast_items = output_forecast_ready(forecast_df)
                display_forecast(forecast_items, unit_symbol)
                display_temperature_chart(forecast_items, unit_symbol)

        elif choice == 3:
            air_pollution = get_current_pollution(lat, lon)
            display_air_pollution(air_pollution)
        
        elif choice == 4:
            current_weather = get_current_weather(lat, lon, units)
            forecast_df = get_forecast_weather(lat, lon, units)

            if isinstance(forecast_df, dict) and forecast_df.get("error"):
                print("Error:", forecast_df.get("message"))
            else:
                forecast_items = output_forecast_ready(forecast_df)
                air_pollution = get_current_pollution(lat, lon)
                display_current_weather(current_weather, unit_symbol)
                display_air_pollution(air_pollution)
                display_forecast(forecast_items, unit_symbol)
                display_temperature_chart(forecast_items, unit_symbol)

        elif choice == 5:
            loc = choose_location()

            if loc:
                lat, lon = loc
            else:
                print("No such location found. Keeping previous location.")

        elif choice == 6:
            units, unit_symbol = choose_units()

        elif choice == 7:
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
