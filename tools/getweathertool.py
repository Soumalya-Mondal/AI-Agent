def get_weather(city: str) -> str:
    """Get the weather for a city."""
    return f'The weather in {city} is sunny.'





# import requests

# API_KEY = ""

# # Get coordinates
# geo_response = requests.get(
#     "https://api.openweathermap.org/geo/1.0/direct",
#     params={
#         "q": "New York",
#         "limit": 1,
#         "appid": API_KEY
#     }
# )

# geo_data = geo_response.json()[0]
# lat = geo_data["lat"]
# lon = geo_data["lon"]

# # Get weather using coordinates
# weather_response = requests.get(
#     "https://api.openweathermap.org/data/2.5/weather",
#     params={
#         "lat": lat,
#         "lon": lon,
#         "appid": API_KEY,
#         "units": "metric"
#     }
# )

# weather = weather_response.json()

# print(weather)