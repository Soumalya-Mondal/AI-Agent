def get_weather(city: str) -> str:
    """
    Retrieve the current weather conditions for a given city.

    Use this tool when the user asks about the weather, temperature, humidity, or
    climate conditions for any city worldwide. Internally resolves the city to
    geographic coordinates and fetches live data from OpenWeatherMap.

    Args:
        city: The name of the city to look up (e.g. "London", "Tokyo", "New York").

    Returns:
        A human-readable string describing the current weather, e.g.
        "The weather in London is clear sky, 15°C, humidity 72%."
        Returns an error message if the city cannot be found or the API request fails.
    """
    # Importing Python Modules:S1
    try:
        import os
        import requests
        import logging
        from config import AppConfig, load_app_config
    except Exception as error:
        # If logging import fails, we still want a meaningful error message.
        print(f"ERROR - [Weather:S1] - {str(error)}")
        return "Unable to Fetch Weather Information"

    # Load Configuration And Validate API Key:S2
    try:
        app_config: AppConfig = load_app_config()
        if not app_config.open_weather_api_key:
            logging.error("ERROR - [Weather:S2] - OPEN_WEATHER_API_KEY missing")
            return "Weather service configuration appears invalid. Please contact support."
    except Exception as error:
        logging.error(f"ERROR - [Weather:S2] - {str(error)}")
        return "Unable to Fetch Weather Information"

    # Calling City's Geo-Coordinate API:S3
    try:
        city_geo_params = {
            "q": city,
            "limit": 1,
            "appid": app_config.open_weather_api_key,
        }
        city_geo_cord_response = requests.get(
            "https://api.openweathermap.org/geo/1.0/direct",
            params=city_geo_params,
            timeout=10,
        )
    except requests.RequestException as error:
        logging.error(f"ERROR - [Weather:S3] - {str(error)}")
        return "Unable to reach the weather service."

    # Fetching City's Geo-Coordinate:S4
    try:
        if city_geo_cord_response.status_code == 200:
            geo_data = city_geo_cord_response.json()
            if not geo_data:
                return (
                    f"I couldn't find weather data for '{city}'. Please check the city name "
                    "or try a nearby major city."
                )
            city_lat = geo_data[0]["lat"]
            city_lon = geo_data[0]["lon"]
        else:
            return "Weather Data Unavailable for the Requested City"
    except Exception as error:
        logging.error(f"ERROR - [Weather:S4] - {str(error)}")
        return "Weather Data Unavailable for the Requested City"

    # Calling City's Weather API:S5
    try:
        city_weather_params = {
            "lat": city_lat,
            "lon": city_lon,
            "units": "metric",
            "appid": app_config.open_weather_api_key,
        }
        city_weather_response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params=city_weather_params,
            timeout=10,
        )
    except requests.RequestException as error:
        logging.error(f"ERROR - [Weather:S5] - {str(error)}")
        return "Unable to reach the weather service."

    # Fetching City's Weather Data:S6
    try:
        if city_weather_response.status_code == 200:
            city_weather_reponse_data = city_weather_response.json()
            return (
                f"The weather in {city} is {city_weather_reponse_data['weather'][0]['description']}, "
                f"{city_weather_reponse_data['main']['temp']}°C (feels like {city_weather_reponse_data['main']['feels_like']}°C, "
                f"min {city_weather_reponse_data['main']['temp_min']}°C, max {city_weather_reponse_data['main']['temp_max']}°C), "
                f"humidity {city_weather_reponse_data['main']['humidity']}%."
            )
        else:
            return "Unable to Fetch Weather Information"
    except Exception as error:
        logging.error(f"ERROR - [Weather:S6] - {str(error)}")
        return "Unable to Fetch Weather Information"
