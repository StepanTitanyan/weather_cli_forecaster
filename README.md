# Weather CLI Forecaster

A simple command-line weather forecast application built with Python.  
The app uses the OpenWeather API to show current weather, 5-day forecast summaries, air quality data, weather icons, and simple temperature charts.

## Features

- Search weather by location name
- Choose between Celsius and Fahrenheit
- View current weather conditions
- View a 5-day forecast summary
- View air quality information
- Simple CLI weather icons
- Temperature trend chart in the terminal
- Caching system to reduce repeated API calls

## Technologies Used

- Python
- OpenWeather API
- Pandas
- Requests
- python-dotenv

## Project Structure

```text
weather_cli/
├── api.py
├── cache.py
├── cli_visuals.py
├── config.py
├── forecast_cleaner.py
├── main.py
├── mapping.py
├── requirements.txt
├── .env.example
└── README.md

## How It Works
The user enters a location name, and the app uses the OpenWeather Geocoding API to find matching locations. After the user selects the correct location, the app can show current weather, forecast data, air quality, or a full report.

The app also stores API responses in a local cache file, so repeated requests for the same location do not always call the API again.

## Notes
The real .env file is included in the repository, please do not share (for security reasons).