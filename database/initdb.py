"""Database initialization helpers."""

# Define "inti_db" Function
def init_db(db_file_path: str) -> None:
    """Initialize the SQLite database and create the conversations table if needed."""

    # Importing Python Module:S1
    try:
        import sqlite3
        from log.logwritter import write_execution_log

        write_execution_log(
            log_message="Init-DB:S1 - Imported sqlite3 and logger modules successfully.",
            step_name="Init-DB:S1",
            log_level="SUCCESS",
        )
    except Exception as error:
        # If imports fail, we still want a meaningful error message.
        print(f"ERROR - [Init-DB:S1] - {str(error)}")
        try:
            write_execution_log(
                log_message=(
                    f"Init-DB:S1 - Failed to import required modules: {str(error)}"
                ),
                step_name="Init-DB:S1",
                log_level="ERROR",
            )
        except Exception:
            pass
        return

    # Create Database Connection Parameter:S2
    try:
        database_connection = sqlite3.connect(db_file_path)
        database_cursor = database_connection.cursor()
        write_execution_log(
            log_message="Init-DB:S2 - Database connection opened successfully.",
            step_name="Init-DB:S2",
            log_level="SUCCESS",
        )
    except Exception as error:
        print(f"ERROR - [Init-DB:S2] - {str(error)}")
        write_execution_log(
            log_message=f"Init-DB:S2 - Failed to open database connection: {str(error)}",
            step_name="Init-DB:S2",
            log_level="ERROR",
        )
        return

    # Create "conversations" Table:S3
    try:
        database_cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_question_text TEXT NOT NULL,
                llm_answer_text TEXT NOT NULL,
                input_token INT NOT NULL,
                output_token INT NOT NULL
            )
            """
        )
        database_connection.commit()
        write_execution_log(
            log_message="Init-DB:S3 - Conversations table ensured successfully.",
            step_name="Init-DB:S3",
            log_level="SUCCESS",
        )
    except Exception as error:
        print(f"ERROR - [Init-DB:S3] - {str(error)}")
        write_execution_log(
            log_message=f"Init-DB:S3 - Failed to create conversations table: {str(error)}",
            step_name="Init-DB:S3",
            log_level="ERROR",
        )
    finally:
        database_connection.close()
