"""Central application configuration module.

Defines AppConfig dataclass and load_app_config helper to read
and validate required environment variables.
"""

# Import Python Modules:S1
try:
    import os
    from dataclasses import dataclass
    from log.logwritter import write_execution_log

    write_execution_log(
        log_message="Config:S1 - Imported configuration modules successfully.",
        step_name="Config:S1",
        log_level="SUCCESS",
    )
except Exception as error:
    # Fallback print; can be replaced by a proper error reporting system if needed
    print(f"ERROR - [Config:S1] - {str(error)}")

    def write_execution_log(
        log_message: str,
        step_name: str = "",
        log_level: str = "SUCCESS",
    ) -> bool:
        return False

    write_execution_log(
        log_message=f"Config:S1 - Failed to import configuration modules: {str(error)}",
        step_name="Config:S1",
        log_level="ERROR",
    )


# Define Config Dataclass:S2
@dataclass
class AppConfig:
    api_endpoint: str
    api_key: str
    api_version: str
    chat_model_name: str
    open_weather_api_key: str
    system_prompt: str


write_execution_log(
    log_message="Config:S2 - AppConfig dataclass defined successfully.",
    step_name="Config:S2",
    log_level="SUCCESS",
)


# Load Configuration From Environment:S3
def load_app_config() -> AppConfig:
    """Load and validate required configuration from environment variables."""
    write_execution_log(
        log_message="Config:S3 - load_app_config execution started.",
        step_name="Config:S3",
        log_level="SUCCESS",
    )

    # Read Environment Variables:S4
    try:
        api_endpoint = os.environ.get("API_ENDPOINT", "").strip()
        api_key = os.environ.get("API_KEY", "").strip()
        api_version = os.environ.get("API_VERSION", "").strip()
        chat_model_name = os.environ.get("CHAT_MODEL_NAME", "").strip()
        open_weather_api_key = os.environ.get("OPEN_WEATHER_API_KEY", "").strip()
        system_prompt = os.environ.get(
            "SYSTEM_PROMPT", "You Are A Helpful Assistant."
        ).strip()
        write_execution_log(
            log_message="Config:S4 - Environment variables read successfully.",
            step_name="Config:S4",
            log_level="SUCCESS",
        )
    except Exception as error:
        write_execution_log(
            log_message=f"Config:S4 - Failed to read environment variables: {str(error)}",
            step_name="Config:S4",
            log_level="ERROR",
        )
        raise

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
        write_execution_log(
            log_message=(
                f"Config:S5 - Missing required environment variables: {missing_str}"
            ),
            step_name="Config:S5",
            log_level="ERROR",
        )
        raise RuntimeError(f"Missing required environment variables: {missing_str}")

    write_execution_log(
        log_message="Config:S5 - Required configuration validated successfully.",
        step_name="Config:S5",
        log_level="SUCCESS",
    )

    # Return Config Object:S6
    app_config = AppConfig(
        api_endpoint=api_endpoint,
        api_key=api_key,
        api_version=api_version,
        chat_model_name=chat_model_name,
        open_weather_api_key=open_weather_api_key,
        system_prompt=system_prompt,
    )
    write_execution_log(
        log_message="Config:S6 - AppConfig object created successfully.",
        step_name="Config:S6",
        log_level="SUCCESS",
    )
    return app_config
