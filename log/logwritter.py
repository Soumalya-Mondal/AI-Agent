# Define "write_execution_log" Function
def write_execution_log(log_message: str, file_name: str, step_number: str, log_level: str = "SUCCESS",) -> bool:
    # Importing Python Modules:S1
    try:
        from datetime import datetime
        from pathlib import Path
        import sqlite3
    except Exception as error:
        print(f"ERROR - [Log-Writter:S1] - {str(error)}")
        return False

    # Validate Input Parameters:S2
    try:
        normalized_message = str(log_message).strip()
        normalized_file_name = str(file_name).strip()
        normalized_step_number = str(step_number).strip().upper()
        normalized_level = str(log_level).strip().upper()
        normalized_status = "ERROR" if normalized_level == "ERROR" else "SUCCESS"

        if not normalized_message:
            print("ERROR - [Log-Writter:S2] - log_message cannot be empty")
            return False

        if not normalized_file_name:
            print("ERROR - [Log-Writter:S2] - file_name cannot be empty")
            return False

        if not normalized_step_number:
            print("ERROR - [Log-Writter:S2] - step_number cannot be empty")
            return False
    except Exception as error:
        print(f"ERROR - [Log-Writter:S2] - {str(error)}")
        return False

    # Define Log File Path:S3
    try:
        log_folder_path = Path(__file__).resolve().parent
        log_folder_path.mkdir(parents=True, exist_ok=True)
        log_db_file_path = log_folder_path / "aiagentlogs.db"
    except Exception as error:
        print(f"ERROR - [Log-Writter:S3] - {str(error)}")
        return False

    # Build Log Payload:S4
    try:
        timestamp_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    except Exception as error:
        print(f"ERROR - [Log-Writter:S4] - {str(error)}")
        return False

    # Write Execution Log Into Database:S5
    try:
        with sqlite3.connect(log_db_file_path) as log_database_connection:
            database_cursor = log_database_connection.cursor()

            database_cursor.execute(
                "INSERT INTO execution_logs (created_at, log_level, file_name, step_number, log_message) VALUES (?, ?, ?, ?, ?)",
                (
                    timestamp_text,
                    normalized_status,
                    normalized_file_name,
                    normalized_step_number,
                    normalized_message,
                ),
            )
            log_database_connection.commit()
        return True
    except Exception as error:
        print(f"ERROR - [Log-Writter:S5] - {str(error)}")
        return False
