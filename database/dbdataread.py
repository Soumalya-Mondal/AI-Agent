"""Database read helpers."""

# Define "get_recent_conversations" Function
def get_recent_conversations(db_file_path: str, limit: int = 10):
    """Return the most recent conversations from the database.

    Results are ordered from newest to oldest based on the auto-incrementing id.
    """

    # Importing Python Modules:S1
    try:
        import sqlite3
    except Exception as error:
        # If imports fail, we still want a meaningful error message.
        print(f"ERROR - [DB-Data-Read:S1] - {str(error)}")
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
            return rows
    except Exception as error:
        print(f"ERROR - [DB-Data-Read:S2] - {str(error)}")
        return []
