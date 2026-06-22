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
        city_geo_cord_response = requests.get(
            'https://api.openweathermap.org/geo/1.0/direct',
            params =
                {'q': city, 'limit': 1, 'appid': str(os.environ.get('OPEN_WEATHER_API_KEY'))},
        )
    except Exception:
        return "Unable to Fetch Weather Information"

    # Fetching City's Geo-Coordinate:S3
    try:
        if (city_geo_cord_response.status_code == 200):
            lat = city_geo_cord_response.json()[0]["lat"]
            lon = city_geo_cord_response.json()[0]["lon"]
        else:
            return "Weather Data Unavailable for the Requested City"
    except Exception:
        return "Weather Data Unavailable for the Requested City"

    # Calling City's Weather API:S4
    try:
        city_weather_response = requests.get(
            'https://api.openweathermap.org/data/2.5/weather',
            params={'lat': lat, 'lon': lon, 'units': 'metric', 'appid': str(os.environ.get('OPEN_WEATHER_API_KEY'))},
        )
    except Exception:
        return "Unable to Fetch Weather Information"

    # Fetching City's Weather Data:S5
    try:
        if (city_weather_response.status_code == 200):
            desc = city_weather_response.json()['weather'][0]['description']
            temp = city_weather_response.json()['main']['temp']
            humidity = city_weather_response.json()['main']['humidity']
            return f"The weather in {city} is {desc}, {temp}°C, humidity {humidity}%."
        else:
            return "Unable to Fetch Weather Information"
    except Exception:
        return "Unable to Fetch Weather Information"