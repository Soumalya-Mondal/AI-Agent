"""Database initialization helpers."""

# Define "inti_db" Function
def init_db(db_file_path: str) -> None:
    """Initialize the SQLite database and create the conversations table if needed."""

    # Importing Python Module:S1
    try:
        import sqlite3
        from pathlib import Path
        from log.logwritter import write_execution_log

        write_execution_log(
            log_message="Init-DB:S1 - Imported sqlite3 and logger modules successfully.",
            file_name="Init-DB",
            step_number="S1",
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
                file_name="Init-DB",
                step_number="S1",
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
            file_name="Init-DB",
            step_number="S2",
            log_level="SUCCESS",
        )
    except Exception as error:
        print(f"ERROR - [Init-DB:S2] - {str(error)}")
        write_execution_log(
            log_message=f"Init-DB:S2 - Failed to open database connection: {str(error)}",
            file_name="Init-DB",
            step_number="S2",
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
            file_name="Init-DB",
            step_number="S3",
            log_level="SUCCESS",
        )
    except Exception as error:
        print(f"ERROR - [Init-DB:S3] - {str(error)}")
        write_execution_log(
            log_message=f"Init-DB:S3 - Failed to create conversations table: {str(error)}",
            file_name="Init-DB",
            step_number="S3",
            log_level="ERROR",
        )

    # Create "execution_logs" Table:S4
    try:
        log_folder_path = Path(__file__).resolve().parent.parent / "log"
        log_folder_path.mkdir(parents=True, exist_ok=True)
        log_db_file_path = log_folder_path / "aiagentlogs.db"

        with sqlite3.connect(log_db_file_path) as log_database_connection:
            log_database_cursor = log_database_connection.cursor()
            log_database_cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='execution_logs'"
            )
            table_exists = log_database_cursor.fetchone() is not None

            create_table_query = """
                CREATE TABLE execution_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    log_level TEXT NOT NULL,
                    file_name TEXT NOT NULL,
                    step_number TEXT NOT NULL,
                    log_message TEXT NOT NULL
                )
            """

            if table_exists:
                log_database_cursor.execute("PRAGMA table_info(execution_logs)")
                existing_columns = [row[1] for row in log_database_cursor.fetchall()]
                has_new_schema = (
                    "file_name" in existing_columns
                    and "step_number" in existing_columns
                    and "step_name" not in existing_columns
                )

                if not has_new_schema:
                    log_database_cursor.execute("DROP TABLE IF EXISTS execution_logs")
                    log_database_cursor.execute(create_table_query)
            else:
                log_database_cursor.execute(create_table_query)

            log_database_connection.commit()

        write_execution_log(
            log_message="Init-DB:S4 - Execution logs table ensured successfully.",
            file_name="Init-DB",
            step_number="S4",
            log_level="SUCCESS",
        )
    except Exception as error:
        print(f"ERROR - [Init-DB:S4] - {str(error)}")
        write_execution_log(
            log_message=(
                f"Init-DB:S4 - Failed to create execution logs table: {str(error)}"
            ),
            file_name="Init-DB",
            step_number="S4",
            log_level="ERROR",
        )
    finally:
        database_connection.close()
