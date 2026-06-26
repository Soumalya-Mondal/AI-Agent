"""Database read helpers."""

# Define "get_recent_conversations" Function
def get_recent_conversations(db_file_path: str, limit: int = 10):
    """Return the most recent conversations from the database.

    Results are ordered from newest to oldest based on the auto-incrementing id.
    """

    # Importing Python Modules:S1
    try:
        import sqlite3
        from log.logwritter import write_execution_log

        write_execution_log(
            log_message="DB-Data-Read:S1 - Imported sqlite3 and logger modules successfully.",
            file_name="DB-Data-Read",
            step_number="S1",
            log_level="SUCCESS",
        )
    except Exception as error:
        # If imports fail, we still want a meaningful error message.
        print(f"ERROR - [DB-Data-Read:S1] - {str(error)}")
        try:
            write_execution_log(
                log_message=(
                    f"DB-Data-Read:S1 - Failed to import required modules: {str(error)}"
                ),
                file_name="DB-Data-Read",
                step_number="S1",
                log_level="ERROR",
            )
        except Exception:
            pass
        return []

    # Fetch Recent Conversations:S2
    try:
        with sqlite3.connect(db_file_path) as database_connection:
            database_cursor = database_connection.cursor()
            database_cursor.execute(
                "SELECT id, user_question_text, llm_answer_text, input_token, output_token FROM conversations ORDER BY id DESC LIMIT ?",
                (limit,),
            )
            rows = database_cursor.fetchall()
            write_execution_log(
                log_message=(
                    f"DB-Data-Read:S2 - Retrieved {len(rows)} conversation rows successfully."
                ),
                file_name="DB-Data-Read",
                step_number="S2",
                log_level="SUCCESS",
            )
            return rows
    except Exception as error:
        print(f"ERROR - [DB-Data-Read:S2] - {str(error)}")
        write_execution_log(
            log_message=(
                f"DB-Data-Read:S2 - Failed to fetch recent conversations: {str(error)}"
            ),
            file_name="DB-Data-Read",
            step_number="S2",
            log_level="ERROR",
        )
        return []
