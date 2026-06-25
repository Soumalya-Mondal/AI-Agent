# Define "get_llm_response" Function
def get_llm_response(user_message: str, db_file_path: str) -> dict:
    # Define Constant
    input_tokens = 0
    output_tokens = 0

    # Importing Python Modules:S1
    try:
        from langchain_openai import AzureChatOpenAI
        from langchain.agents import create_agent
        from langchain_core.messages import HumanMessage
        from pydantic import SecretStr
        from tools.getweathertool import get_weather
        from database.dbdatainsert import insert_conversation
        from supportscript.config import AppConfig, load_app_config
        from log.logwritter import write_execution_log

        write_execution_log(
            log_message="LLM-Response:S1 - Imported LLM response modules successfully.",
            step_name="LLM-Response:S1",
            log_level="SUCCESS",
        )
    except Exception as error:
        # If imports fail, we still want a meaningful error message.
        print(f"ERROR - [LLM-Response:S1] - {str(error)}")
        try:
            write_execution_log(
                log_message=(
                    f"LLM-Response:S1 - Failed to import LLM response modules: {str(error)}"
                ),
                step_name="LLM-Response:S1",
                log_level="ERROR",
            )
        except Exception:
            pass
        return {
            "status": "ERROR",
            "error_code": "IMPORT_ERROR",
            "message": str(error),
            "assistant_message": "No Response Generated",
            "input_tokens": 0,
            "output_tokens": 0,
        }

    # Create Azure LLM Object:S2
    try:
        app_config: AppConfig = load_app_config()
        azure_llm_object = AzureChatOpenAI(
            azure_endpoint=app_config.api_endpoint,
            api_key=SecretStr(app_config.api_key),
            api_version=app_config.api_version,
            azure_deployment=app_config.chat_model_name,
            temperature=0,
        )
        write_execution_log(
            log_message="LLM-Response:S2 - Azure LLM object created successfully.",
            step_name="LLM-Response:S2",
            log_level="SUCCESS",
        )
    except Exception as error:
        print(f"ERROR - [LLM-Response:S2] - {str(error)}")
        write_execution_log(
            log_message=f"LLM-Response:S2 - Failed to create Azure LLM object: {str(error)}",
            step_name="LLM-Response:S2",
            log_level="ERROR",
        )
        return {
            "status": "ERROR",
            "error_code": "MODEL_ERROR",
            "message": str(error),
            "assistant_message": "No Response Generated",
            "input_tokens": 0,
            "output_tokens": 0,
        }

    # Calling LLM Agent:S3
    try:
        app_config: AppConfig = load_app_config()
        llm_agent = create_agent(
            model=azure_llm_object,
            tools=[get_weather],
            system_prompt=(
                app_config.system_prompt
                + "\nIf the user asks about current weather, temperature, humidity, or climate in any city, use the get_weather tool instead of guessing."
                + "\nWhen you use get_weather, return the tool output exactly as-is and do not use markdown formatting."
            ),
        )
        write_execution_log(
            log_message="LLM-Response:S3 - LLM agent created successfully.",
            step_name="LLM-Response:S3",
            log_level="SUCCESS",
        )
    except Exception as error:
        print(f"ERROR - [LLM-Response:S3] - {str(error)}")
        write_execution_log(
            log_message=f"LLM-Response:S3 - Failed to create LLM agent: {str(error)}",
            step_name="LLM-Response:S3",
            log_level="ERROR",
        )
        return {
            "status": "ERROR",
            "error_code": "AGENT_ERROR",
            "message": str(error),
            "assistant_message": "No Response Generated",
            "input_tokens": 0,
            "output_tokens": 0,
        }

    # Define "_message_content_to_text" Function:S4
    try:
        def _message_content_to_text(content: object) -> str:
            if isinstance(content, str):
                return content.strip()

            if isinstance(content, list):
                text_parts = []
                for item in content:
                    if isinstance(item, str):
                        normalized_text = item.strip()
                        if normalized_text:
                            text_parts.append(normalized_text)
                    elif isinstance(item, dict):
                        item_text = item.get("text", "")
                        if isinstance(item_text, str):
                            normalized_text = item_text.strip()
                            if normalized_text:
                                text_parts.append(normalized_text)
                return " ".join(text_parts).strip()

            if content is None:
                return ""

            return str(content).strip()
        write_execution_log(
            log_message="LLM-Response:S4 - _message_content_to_text defined successfully.",
            step_name="LLM-Response:S4",
            log_level="SUCCESS",
        )
    except Exception as error:
        print(f"ERROR - [LLM-Response:S4] - {str(error)}")
        write_execution_log(
            log_message=(
                f"LLM-Response:S4 - Failed to define _message_content_to_text: {str(error)}"
            ),
            step_name="LLM-Response:S4",
            log_level="ERROR",
        )
        return {
            "status": "ERROR",
            "error_code": "MESSAGE_CONTENT_TO_TEXT_ERROR",
            "message": str(error),
            "assistant_message": "No Response Generated",
            "input_tokens": 0,
            "output_tokens": 0,
        }

    # Define "select_assistant_message" Function:S5
    try:
        def select_assistant_message(messages: list) -> str:
            if not messages:
                return "No Response Generated"

            fallback_response = _message_content_to_text(
                getattr(messages[-1], "content", "")
            )
            if not fallback_response:
                fallback_response = "No Response Generated"

            for message in reversed(messages):
                if getattr(message, "type", "") == "tool":
                    tool_response = _message_content_to_text(
                        getattr(message, "content", "")
                    )
                    if tool_response:
                        return tool_response

            return fallback_response
        write_execution_log(
            log_message="LLM-Response:S5 - select_assistant_message defined successfully.",
            step_name="LLM-Response:S5",
            log_level="SUCCESS",
        )
    except Exception as error:
        print(f"ERROR - [LLM-Response:S5] - {str(error)}")
        write_execution_log(
            log_message=(
                f"LLM-Response:S5 - Failed to define select_assistant_message: {str(error)}"
            ),
            step_name="LLM-Response:S5",
            log_level="ERROR",
        )
        return {
            "status": "ERROR",
            "error_code": "SELECT_ASSISTANT_MESSAGE_ERROR",
            "message": str(error),
            "assistant_message": "No Response Generated",
            "input_tokens": 0,
            "output_tokens": 0,
        }

    # Generate LLM Response:S6
    try:
        llm_response = llm_agent.invoke({"messages": [HumanMessage(content=user_message)]})
        response_messages = llm_response["messages"]
        assistant_response = select_assistant_message(response_messages)
        last_message = response_messages[-1]
        if hasattr(last_message, "usage_metadata") and last_message.usage_metadata:
            usage = last_message.usage_metadata
            input_tokens = (
                usage.get("input_tokens", 0)
                if isinstance(usage, dict)
                else getattr(usage, "input_tokens", 0)
            )
            output_tokens = (
                usage.get("output_tokens", 0)
                if isinstance(usage, dict)
                else getattr(usage, "output_tokens", 0)
            )
        write_execution_log(
            log_message="LLM-Response:S6 - LLM response generated successfully.",
            step_name="LLM-Response:S6",
            log_level="SUCCESS",
        )
    except Exception as error:
        print(f"ERROR - [LLM-Response:S6] - {str(error)}")
        write_execution_log(
            log_message=f"LLM-Response:S6 - Failed to invoke LLM agent: {str(error)}",
            step_name="LLM-Response:S6",
            log_level="ERROR",
        )
        return {
            "status": "ERROR",
            "error_code": "INVOCATION_ERROR",
            "message": str(error),
            "assistant_message": "No Response Generated",
            "input_tokens": 0,
            "output_tokens": 0,
        }

    # Insert Response Into Database:S7
    try:
        insert_conversation(
            db_file_path=db_file_path,
            user_question_text=user_message,
            llm_answer_text=assistant_response,
            input_token=input_tokens,
            output_token=output_tokens,
        )
        write_execution_log(
            log_message="LLM-Response:S7 - Conversation inserted into database successfully.",
            step_name="LLM-Response:S7",
            log_level="SUCCESS",
        )
    except Exception as error:
        print(f"ERROR - [LLM-Response:S7] - {str(error)}")
        write_execution_log(
            log_message=(
                f"LLM-Response:S7 - Failed to insert conversation into database: {str(error)}"
            ),
            step_name="LLM-Response:S7",
            log_level="ERROR",
        )
        return {
            "status": "ERROR",
            "error_code": "DB_ERROR",
            "message": str(error),
            "assistant_message": assistant_response,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
        }

    # Sending Final Message To Main Function:S8
    write_execution_log(
        log_message="LLM-Response:S8 - Returning successful response payload.",
        step_name="LLM-Response:S8",
        log_level="SUCCESS",
    )
    return {
        "status": "SUCCESS",
        "message": "Success",
        "assistant_message": assistant_response,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
    }
