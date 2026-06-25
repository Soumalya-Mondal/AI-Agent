"""Central application configuration module.

Defines AppConfig dataclass and load_app_config helper to read
and validate required environment variables.
"""

# Import Python Modules:S1
try:
    import os
    from dataclasses import dataclass
except Exception as error:
    # Fallback print; will be replaced by logging once logging is configured
    print(f"ERROR - [Config:S1] - {str(error)}")


# Define Config Dataclass:S2
@dataclass
class AppConfig:
    api_endpoint: str
    api_key: str
    api_version: str
    chat_model_name: str
    open_weather_api_key: str
    system_prompt: str


# Load Configuration From Environment:S3
def load_app_config() -> AppConfig:
    """Load and validate required configuration from environment variables."""
    # Read Environment Variables:S4
    api_endpoint = os.environ.get("API_ENDPOINT", "").strip()
    api_key = os.environ.get("API_KEY", "").strip()
    api_version = os.environ.get("API_VERSION", "").strip()
    chat_model_name = os.environ.get("CHAT_MODEL_NAME", "").strip()
    open_weather_api_key = os.environ.get("OPEN_WEATHER_API_KEY", "").strip()
    system_prompt = os.environ.get(
        "SYSTEM_PROMPT", "You Are A Helpful Assistant."
    ).strip()

    # Validate Required Configuration:S5
    missing = []
    if not api_endpoint:
        missing.append("API_ENDPOINT")
    if not api_key:
        missing.append("API_KEY")
    if not api_version:
        missing.append("API_VERSION")
    if not chat_model_name:
        missing.append("CHAT_MODEL_NAME")
    if not open_weather_api_key:
        missing.append("OPEN_WEATHER_API_KEY")

    if missing:
        missing_str = ", ".join(missing)
        raise RuntimeError(f"Missing required environment variables: {missing_str}")

    # Return Config Object:S6
    return AppConfig(
        api_endpoint=api_endpoint,
        api_key=api_key,
        api_version=api_version,
        chat_model_name=chat_model_name,
        open_weather_api_key=open_weather_api_key,
        system_prompt=system_prompt,
    )
