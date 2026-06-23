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
    except Exception:
        return "Unable to Fetch Weather Information"

    # Calling City's Geo-Coordinate API:S2
    try:
        city_geo_params = {
            'q': city,
            'limit': 1,
            'appid': str(os.environ.get('OPEN_WEATHER_API_KEY')),
        }
        city_geo_cord_response = requests.get(
            'https://api.openweathermap.org/geo/1.0/direct',
            params = city_geo_params,
        )
    except Exception:
        return "Unable to Fetch Weather Information"

    # Fetching City's Geo-Coordinate:S3
    try:
        if (city_geo_cord_response.status_code == 200):
            city_lat = city_geo_cord_response.json()[0]["lat"]
            city_lon = city_geo_cord_response.json()[0]["lon"]
        else:
            return "Weather Data Unavailable for the Requested City"
    except Exception:
        return "Weather Data Unavailable for the Requested City"

    # Calling City's Weather API:S4
    try:
        city_weather_params = {
            'lat': city_lat,
            'lon': city_lon,
            'units': 'metric',
            'appid': str(os.environ.get('OPEN_WEATHER_API_KEY')),
        }
        city_weather_response = requests.get(
            'https://api.openweathermap.org/data/2.5/weather',
            params = city_weather_params,
        )
    except Exception:
        return "Unable to Fetch Weather Information"

    # Fetching City's Weather Data:S5
    try:
        if (city_weather_response.status_code == 200):
            city_weather_reponse_data = city_weather_response.json()
            return f"The weather in {city} is {city_weather_reponse_data['weather'][0]['description']}, {city_weather_reponse_data['main']['temp']}°C (feels like {city_weather_reponse_data['main']['feels_like']}°C, min {city_weather_reponse_data['main']['temp_min']}°C, max {city_weather_reponse_data['main']['temp_max']}°C), humidity {city_weather_reponse_data['main']['humidity']}%."
        else:
            return "Unable to Fetch Weather Information"
    except Exception:
        return "Unable to Fetch Weather Information"