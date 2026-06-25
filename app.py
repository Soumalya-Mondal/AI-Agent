# Import Python Modules:S1
try:
    from flask import Flask, request, jsonify, render_template
    from pathlib import Path
    from dotenv import load_dotenv
    from log.logwritter import write_execution_log

    write_execution_log(
        log_message="Main:S1 - Imported Python modules successfully.",
        step_name="Main:S1",
        log_level="SUCCESS",
    )
except Exception as error:
    print(f"ERROR - [Main:S1] - {str(error)}")

    def write_execution_log(
        log_message: str,
        step_name: str = "",
        log_level: str = "SUCCESS",
    ) -> bool:
        return False

    try:
        write_execution_log(
            log_message=f"Main:S1 - Failed to import Python modules: {str(error)}",
            step_name="Main:S1",
            log_level="ERROR",
        )
    except Exception:
        pass

# Import Modules:S2
try:
    from supportscript.llmresponse import get_llm_response
    from database.initdb import init_db
    from database.dbdataread import get_recent_conversations
    from supportscript.config import load_app_config, AppConfig

    write_execution_log(
        log_message="Main:S2 - Imported application modules successfully.",
        step_name="Main:S2",
        log_level="SUCCESS",
    )
except Exception as error:
    print(f'ERROR - [Main:S2] - {str(error)}')
    try:
        write_execution_log(
            log_message=f"Main:S2 - Failed to import application modules: {str(error)}",
            step_name="Main:S2",
            log_level="ERROR",
        )
    except Exception:
        pass

# Note: Logging has been removed. Errors and informational messages
# are reported using simple print statements instead.

# Define Flask Object:S3
try:
    app = Flask(
        __name__,
        template_folder="frontend",
        static_folder="frontend/static",
        static_url_path="/static",
    )
    write_execution_log(
        log_message="Main:S3 - Flask app object created successfully.",
        step_name="Main:S3",
        log_level="SUCCESS",
    )
except Exception as error:
    print(f"ERROR - [Main:S3] - {str(error)}")
    write_execution_log(
        log_message=f"Main:S3 - Failed to create Flask app object: {str(error)}",
        step_name="Main:S3",
        log_level="ERROR",
    )

# Define Folder And File Path:S4
try:
    parent_folder_path = Path.cwd()
    env_file_path = parent_folder_path / ".env"
    database_folder_path = parent_folder_path / "database"
    database_file_path = database_folder_path / "chat_conversations.db"
    write_execution_log(
        log_message="Main:S4 - Application paths resolved successfully.",
        step_name="Main:S4",
        log_level="SUCCESS",
    )
except Exception as error:
    print(f"ERROR - [Main:S4] - {str(error)}")
    write_execution_log(
        log_message=f"Main:S4 - Failed to resolve application paths: {str(error)}",
        step_name="Main:S4",
        log_level="ERROR",
    )

# Load Environment Variables at OS Level:S5
try:
    load_dotenv(dotenv_path=env_file_path)
    app_config: AppConfig = load_app_config()
    print("INFO - [Main:S5] - Application configuration loaded successfully")
    write_execution_log(
        log_message="Main:S5 - Environment variables and application configuration loaded successfully.",
        step_name="Main:S5",
        log_level="SUCCESS",
    )
except Exception as error:
    print(f"ERROR - [Main:S5] - Failed to load configuration: {str(error)}")
    write_execution_log(
        log_message=f"Main:S5 - Failed to load configuration: {str(error)}",
        step_name="Main:S5",
        log_level="ERROR",
    )
    raise

# Initialize Database:S6
try:
    if not database_file_path.exists():
        init_db(str(database_file_path))
        write_execution_log(
            log_message="Main:S6 - Database initialized successfully.",
            step_name="Main:S6",
            log_level="SUCCESS",
        )
    else:
        write_execution_log(
            log_message="Main:S6 - Database already present; initialization skipped.",
            step_name="Main:S6",
            log_level="SUCCESS",
        )
except Exception as error:
    print(f"ERROR - [Main:S6] - {str(error)}")
    write_execution_log(
        log_message=f"Main:S6 - Database initialization failed: {str(error)}",
        step_name="Main:S6",
        log_level="ERROR",
    )


# Route to serve the chat interface
@app.route('/')
def index():
    return render_template('index.html')

# API Route to handle chat messages
@app.route("/api/chat", methods=["POST"])
def chat():
    # Fetch User Message From Request and Call Agent to Generate Response:S7
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        # Check If The User Message Is Not Empty
        if not user_message:
            write_execution_log(
                log_message="Main:S7 - Received empty user message.",
                step_name="Main:S7",
                log_level="ERROR",
            )
            return jsonify({"error": "Message Cannot Be Empty"}), 400

        # Calling "get_llm_response" Function For Answer Generation
        llm_response_result = get_llm_response(
            user_message=user_message, db_file_path=str(database_file_path)
        )

        if llm_response_result["status"] == "SUCCESS":
            write_execution_log(
                log_message="Main:S7 - Chat response generated successfully.",
                step_name="Main:S7",
                log_level="SUCCESS",
            )
            return jsonify({
                "response": llm_response_result["assistant_message"],
                "input_tokens": llm_response_result["input_tokens"],
                "output_tokens": llm_response_result["output_tokens"],
            }), 200
        else:
            error_code = llm_response_result.get("error_code", "UNKNOWN_ERROR")
            message = llm_response_result.get(
                "message", "Failed To Generate Response"
            )

            status_code = 500
            if error_code in ("CONFIG_ERROR", "IMPORT_ERROR"):
                status_code = 500
            elif error_code in (
                "MODEL_ERROR",
                "AGENT_ERROR",
                "INVOCATION_ERROR",
                "DB_ERROR",
            ):
                status_code = 502

            write_execution_log(
                log_message=(
                    f"Main:S7 - Chat response failed with {error_code}: {message}"
                ),
                step_name="Main:S7",
                log_level="ERROR",
            )
            return jsonify({"error": message, "error_code": error_code}), status_code
    except Exception as error:
        print(f"ERROR - [Main:S7] - {str(error)}")
        write_execution_log(
            log_message=f"Main:S7 - Unexpected chat route error: {str(error)}",
            step_name="Main:S7",
            log_level="ERROR",
        )
        return jsonify(
            {"error": "Failed To Generate Response", "error_code": "UNKNOWN_ERROR"}
        ), 500


# Health Check Route:S8
@app.route("/health")
def health():
    try:
        # Simple health check: configuration and DB file existence
        _ = app_config  # ensure config is loaded
        if not database_file_path.exists():
            write_execution_log(
                log_message="Main:S8 - Health check failed because database file is missing.",
                step_name="Main:S8",
                log_level="ERROR",
            )
            return jsonify(
                {"status": "error", "details": "Database file missing"}
            ), 500
        write_execution_log(
            log_message="Main:S8 - Health check completed successfully.",
            step_name="Main:S8",
            log_level="SUCCESS",
        )
        return jsonify({"status": "ok"}), 200
    except Exception as error:
        print(f"ERROR - [Main:S8] - {str(error)}")
        write_execution_log(
            log_message=f"Main:S8 - Health check raised exception: {str(error)}",
            step_name="Main:S8",
            log_level="ERROR",
        )
        return jsonify(
            {"status": "error", "details": "Health check failed"}
        ), 500


# History API Route:S9
@app.route("/api/history", methods=["GET"])
def history():
    try:
        limit_param = request.args.get("limit", "10")
        try:
            limit = int(limit_param)
        except ValueError:
            limit = 10

        rows = get_recent_conversations(str(database_file_path), limit=limit)
        history_data = [
            {
                "id": row[0],
                "user_question_text": row[1],
                "llm_answer_text": row[2],
                "input_token": row[3],
                "output_token": row[4],
            }
            for row in rows
        ]
        write_execution_log(
            log_message=(
                f"Main:S9 - History fetched successfully with {len(history_data)} records."
            ),
            step_name="Main:S9",
            log_level="SUCCESS",
        )
        return jsonify({"conversations": history_data}), 200
    except Exception as error:
        print(f"ERROR - [Main:S9] - {str(error)}")
        write_execution_log(
            log_message=f"Main:S9 - Failed to fetch history: {str(error)}",
            step_name="Main:S9",
            log_level="ERROR",
        )
        return jsonify({"error": "Failed To Fetch History"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
