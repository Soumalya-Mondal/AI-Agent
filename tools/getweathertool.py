def format_weather_summary(city: str, weather_data: dict) -> str:
    """Return a consistent plain-text weather summary sentence."""
    return (
        f"The weather in {city} is currently {weather_data['weather'][0]['description']}, "
        f"around {weather_data['main']['temp']}°C (feels like {weather_data['main']['feels_like']}°C), "
        f"with about {weather_data['main']['humidity']}% humidity."
    )


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
        import requests
        from supportscript.config import AppConfig, load_app_config
        from log.logwritter import write_execution_log

        write_execution_log(
            log_message="Weather:S1 - Imported weather dependencies successfully.",
            step_name="Weather:S1",
            log_level="SUCCESS",
        )
    except Exception as error:
        # If imports fail, we still want a meaningful error message.
        print(f"ERROR - [Weather:S1] - {str(error)}")
        try:
            write_execution_log(
                log_message=(
                    f"Weather:S1 - Failed to import weather dependencies: {str(error)}"
                ),
                step_name="Weather:S1",
                log_level="ERROR",
            )
        except Exception:
            pass
        return "Unable to Fetch Weather Information"

    # Load Configuration And Validate API Key:S2
    try:
        app_config: AppConfig = load_app_config()
        if not app_config.open_weather_api_key:
            print("ERROR - [Weather:S2] - OPEN_WEATHER_API_KEY missing")
            write_execution_log(
                log_message="Weather:S2 - OPEN_WEATHER_API_KEY is missing.",
                step_name="Weather:S2",
                log_level="ERROR",
            )
            return "Weather service configuration appears invalid. Please contact support."
        resolved_city_name = city
        write_execution_log(
            log_message="Weather:S2 - Weather configuration loaded successfully.",
            step_name="Weather:S2",
            log_level="SUCCESS",
        )
    except Exception as error:
        print(f"ERROR - [Weather:S2] - {str(error)}")
        write_execution_log(
            log_message=f"Weather:S2 - Failed to load weather configuration: {str(error)}",
            step_name="Weather:S2",
            log_level="ERROR",
        )
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
        write_execution_log(
            log_message="Weather:S3 - Geo-coordinate API called successfully.",
            step_name="Weather:S3",
            log_level="SUCCESS",
        )
    except requests.RequestException as error:
        print(f"ERROR - [Weather:S3] - {str(error)}")
        write_execution_log(
            log_message=f"Weather:S3 - Failed to call geo-coordinate API: {str(error)}",
            step_name="Weather:S3",
            log_level="ERROR",
        )
        return "Unable to reach the weather service."

    # Fetching City's Geo-Coordinate:S4
    try:
        if city_geo_cord_response.status_code == 200:
            geo_data = city_geo_cord_response.json()
            if not geo_data:
                write_execution_log(
                    log_message=(
                        f"Weather:S4 - No geo-coordinate data found for city '{city}'."
                    ),
                    step_name="Weather:S4",
                    log_level="ERROR",
                )
                return (
                    f"I couldn't find weather data for '{city}'. Please check the city name "
                    "or try a nearby major city."
                )
            city_lat = geo_data[0]["lat"]
            city_lon = geo_data[0]["lon"]
            resolved_city_name = geo_data[0].get("name", city)
            write_execution_log(
                log_message="Weather:S4 - City geo-coordinates resolved successfully.",
                step_name="Weather:S4",
                log_level="SUCCESS",
            )
        else:
            write_execution_log(
                log_message=(
                    "Weather:S4 - Geo-coordinate API returned non-200 status code."
                ),
                step_name="Weather:S4",
                log_level="ERROR",
            )
            return "Weather Data Unavailable for the Requested City"
    except Exception as error:
        print(f"ERROR - [Weather:S4] - {str(error)}")
        write_execution_log(
            log_message=f"Weather:S4 - Failed to parse geo-coordinate response: {str(error)}",
            step_name="Weather:S4",
            log_level="ERROR",
        )
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
        write_execution_log(
            log_message="Weather:S5 - Weather API called successfully.",
            step_name="Weather:S5",
            log_level="SUCCESS",
        )
    except requests.RequestException as error:
        print(f"ERROR - [Weather:S5] - {str(error)}")
        write_execution_log(
            log_message=f"Weather:S5 - Failed to call weather API: {str(error)}",
            step_name="Weather:S5",
            log_level="ERROR",
        )
        return "Unable to reach the weather service."

    # Fetching City's Weather Data:S6
    try:
        if city_weather_response.status_code == 200:
            city_weather_reponse_data = city_weather_response.json()
            write_execution_log(
                log_message="Weather:S6 - Weather data fetched successfully.",
                step_name="Weather:S6",
                log_level="SUCCESS",
            )
            return format_weather_summary(
                city=resolved_city_name,
                weather_data=city_weather_reponse_data,
            )
        else:
            write_execution_log(
                log_message="Weather:S6 - Weather API returned non-200 status code.",
                step_name="Weather:S6",
                log_level="ERROR",
            )
            return "Unable to Fetch Weather Information"
    except Exception as error:
        print(f"ERROR - [Weather:S6] - {str(error)}")
        write_execution_log(
            log_message=f"Weather:S6 - Failed to parse weather response: {str(error)}",
            step_name="Weather:S6",
            log_level="ERROR",
        )
        return "Unable to Fetch Weather Information"
