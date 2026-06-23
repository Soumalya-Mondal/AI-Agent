# Define "insert_conversation" Function
def insert_conversation(db_file_path: str, user_question_text: str, llm_answer_text: str, input_token: int, output_token: int) -> None:
    # Importing Python Modules:S1
    try:
        import sqlite3
    except Exception as error:
        print(f'ERROR - [DB-Data-Insert:S1] - {str(error)}')

    # Create Database Connection Parameter:S2
    try:
        database_connection = sqlite3.connect(db_file_path)
        database_cursor = database_connection.cursor()
    except Exception as error:
        print(f'ERROR - [DB-Data-Insert:S2] - {str(error)}')

    # Insert Data into "conversations" Table:S3
    try:
        database_cursor.execute(
            'INSERT INTO conversations (user_question_text, llm_answer_text, input_token, output_token) VALUES (?, ?, ?, ?)',
            (user_question_text, llm_answer_text, input_token, output_token)
        )
        database_connection.commit()
    except Exception as error:
        print(f'ERROR - [DB-Data-Insert:S3] - {str(error)}')
    finally:
        database_connection.close()
