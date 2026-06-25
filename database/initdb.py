"""Database initialization helpers."""

# Define "inti_db" Function
def init_db(db_file_path: str) -> None:
    """Initialize the SQLite database and create the conversations table if needed."""

    # Importing Python Module:S1
    try:
        import sqlite3
        import logging
    except Exception as error:
        # If logging import fails, we still want a meaningful error message.
        print(f"ERROR - [Init-DB:S1] - {str(error)}")
        return

    # Create Database Connection Parameter:S2
    try:
        database_connection = sqlite3.connect(db_file_path)
        database_cursor = database_connection.cursor()
    except Exception as error:
        logging.error(f"ERROR - [Init-DB:S2] - {str(error)}")
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
    except Exception as error:
        logging.error(f"ERROR - [Init-DB:S3] - {str(error)}")
    finally:
        database_connection.close()
