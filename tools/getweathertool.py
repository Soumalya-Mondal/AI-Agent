def get_weather(city: str) -> str | None:
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
        Returns None if the city cannot be found or the API request fails.
    """

    # Importing Python Modules:S1
    try:
        import os
        import requests
    except Exception as error:
        print(f'ERROR - [Get-Weather:S1] - {str(error)}')

    # Calling City's Geo-Coordinate API:S2
    try:
        geo_response = requests.get(
            'https://api.openweathermap.org/geo/1.0/direct',
            params =
                {'q': city, 'limit': 1, 'appid': str(os.environ.get('OPEN_WEATHER_API_KEY'))},
        )
    except Exception as error:
        print(f'ERROR - [Get-Weather:S2] - {str(error)}')

    # Fetching City's Geo-Coordinate:S3
    try:
        if geo_response.status_code == 200:
            lat = geo_response.json()[0]["lat"]
            lon = geo_response.json()[0]["lon"]
    except Exception as error:
        print(f'ERROR - [Get-Weather:S3] - {str(error)}')

    # Calling City's Weather API:S4
    try:
        weather_response = requests.get(
            'https://api.openweathermap.org/data/2.5/weather',
            params={'lat': lat, 'lon': lon, 'units': 'metric', 'appid': str(os.environ.get('OPEN_WEATHER_API_KEY'))},
        )
    except Exception as error:
        print(f'ERROR - [Get-Weather:S4] - {str(error)}')

    # Fetching City's Weather Data:S5
    try:
        if weather_response.status_code == 200:
            desc = weather_response.json()['weather'][0]['description']
            temp = weather_response.json()['main']['temp']
            humidity = weather_response.json()['main']['humidity']
            return f"The weather in {city} is {desc}, {temp}°C, humidity {humidity}%."
    except Exception as error:
        print(f'ERROR - [Get-Weather:S5] - {str(error)}')