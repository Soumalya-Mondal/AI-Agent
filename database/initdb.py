# Define "inti_db" Function
def init_db(db_file_path: str) -> None:
    # Importing Python Module:S1
    try:
        import sqlite3
    except Exception as error:
        print(f'ERROR - [Init-DB:S1] - {str(error)}')

    # Create Database Connection Parameter:S2
    try:
        database_connection = sqlite3.connect(db_file_path)
        database_cursor = database_connection.cursor()
    except Exception as error:
        print(f'ERROR - [Init-DB:S2] - {str(error)}')

    # Create "conversations" Table:S3
    try:
        database_cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_question_text TEXT NOT NULL,
                llm_answer_text TEXT NOT NULL,
                input_token INT NOT NULL,
                output_token INT NOT NULL
            )
        ''')
        database_connection.commit()
    except Exception as error:
        print(f'ERROR - [Init-DB:S3] - {str(error)}')
    finally:
        database_connection.close()