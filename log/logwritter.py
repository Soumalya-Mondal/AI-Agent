"""Execution log writing helpers."""


# Define "write_execution_log" Function
def write_execution_log(
    log_message: str,
    step_name: str = "",
    log_level: str = "SUCCESS",
) -> bool:
    """Write a single log line in `local time - SUCCESS/ERROR - MESSAGE` format."""

    # Importing Python Modules:S1
    try:
        from datetime import datetime
        from pathlib import Path
    except Exception as error:
        print(f"ERROR - [Log-Writter:S1] - {str(error)}")
        return False

    # Validate Input Parameters:S2
    try:
        normalized_message = str(log_message).strip()
        _ = str(step_name).strip()
        normalized_level = str(log_level).strip().upper()
        normalized_status = "ERROR" if normalized_level == "ERROR" else "SUCCESS"

        if not normalized_message:
            print("ERROR - [Log-Writter:S2] - log_message cannot be empty")
            return False
    except Exception as error:
        print(f"ERROR - [Log-Writter:S2] - {str(error)}")
        return False

    # Define Log File Path:S3
    try:
        log_folder_path = Path(__file__).resolve().parent
        log_folder_path.mkdir(parents=True, exist_ok=True)
        log_file_path = log_folder_path / "aiagent.log"
        log_file_path.touch(exist_ok=True)
    except Exception as error:
        print(f"ERROR - [Log-Writter:S3] - {str(error)}")
        return False

    # Build Log Line:S4
    try:
        timestamp_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"{timestamp_text} - {normalized_status} - {normalized_message}\n"
    except Exception as error:
        print(f"ERROR - [Log-Writter:S4] - {str(error)}")
        return False

    # Write Execution Log Into File:S5
    try:
        with log_file_path.open("a", encoding="utf-8") as log_file:
            log_file.write(log_line)
        return True
    except Exception as error:
        print(f"ERROR - [Log-Writter:S5] - {str(error)}")
        return False
