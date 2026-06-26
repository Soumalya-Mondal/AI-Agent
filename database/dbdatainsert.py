"""Database write helpers."""

# Define "insert_conversation" Function
def insert_conversation(
    db_file_path: str,
    user_question_text: str,
    llm_answer_text: str,
    input_token: int,
    output_token: int,
) -> None:
    """Insert a single conversation row into the conversations table."""

    # Importing Python Modules:S1
    try:
        import sqlite3
        from log.logwritter import write_execution_log

        write_execution_log(
            log_message="DB-Data-Insert:S1 - Imported sqlite3 and logger modules successfully.",
            file_name="DB-Data-Insert",
            step_number="S1",
            log_level="SUCCESS",
        )
    except Exception as error:
        # If imports fail, we still want a meaningful error message.
        print(f"ERROR - [DB-Data-Insert:S1] - {str(error)}")
        try:
            write_execution_log(
                log_message=(
                    f"DB-Data-Insert:S1 - Failed to import required modules: {str(error)}"
                ),
                file_name="DB-Data-Insert",
                step_number="S1",
                log_level="ERROR",
            )
        except Exception:
            pass
        return

    # Create Database Connection Parameter:S2
    try:
        with sqlite3.connect(db_file_path) as database_connection:
            database_cursor = database_connection.cursor()
            write_execution_log(
                log_message="DB-Data-Insert:S2 - Database connection created successfully.",
                file_name="DB-Data-Insert",
                step_number="S2",
                log_level="SUCCESS",
            )

            # Insert Data into "conversations" Table:S3
            try:
                database_cursor.execute(
                    "INSERT INTO conversations (user_question_text, llm_answer_text, input_token, output_token) VALUES (?, ?, ?, ?)",
                    (user_question_text, llm_answer_text, input_token, output_token),
                )
                database_connection.commit()
                write_execution_log(
                    log_message="DB-Data-Insert:S3 - Conversation inserted successfully.",
                    file_name="DB-Data-Insert",
                    step_number="S3",
                    log_level="SUCCESS",
                )
            except Exception as error:
                print(f"ERROR - [DB-Data-Insert:S3] - {str(error)}")
                write_execution_log(
                    log_message=(
                        f"DB-Data-Insert:S3 - Failed to insert conversation: {str(error)}"
                    ),
                    file_name="DB-Data-Insert",
                    step_number="S3",
                    log_level="ERROR",
                )
    except Exception as error:
        print(f"ERROR - [DB-Data-Insert:S2] - {str(error)}")
        write_execution_log(
            log_message=(
                f"DB-Data-Insert:S2 - Failed to create database connection: {str(error)}"
            ),
            file_name="DB-Data-Insert",
            step_number="S2",
            log_level="ERROR",
        )
