# Define "get_llm_response" Function
def get_llm_response(user_message: str, db_file_path: str) -> dict:
    # Define Constant
    input_tokens = 0
    output_tokens = 0

    # Importing Python Modules:S1
    try:
        import os
        from langchain_openai import AzureChatOpenAI
        from langchain.agents import create_agent
        from langchain_core.messages import HumanMessage
        from pydantic import SecretStr
        from tools.getweathertool import get_weather
        from database.dbdatainsert import insert_conversation
    except Exception as error:
        return {'status': 'ERROR', 'message': str(error), 'assistant_message': 'No Response Generated', 'input_tokens': 0, 'output_tokens': 0}

    # Create Azure LLM Object:S2
    try:
        azure_llm_object = AzureChatOpenAI(
            azure_endpoint = os.environ.get('API_ENDPOINT'),
            api_key = SecretStr(str(os.environ.get('API_KEY'))) if os.environ.get('API_KEY') else None,
            api_version = os.environ.get('API_VERSION'),
            azure_deployment = os.environ.get('CHAT_MODEL_NAME'),
            temperature = 0
        )
    except Exception as error:
        return {'status': 'ERROR', 'message': str(error), 'assistant_message': 'No Response Generated', 'input_tokens': 0, 'output_tokens': 0}

    # Calling LLM Agent:S3
    try:
        llm_agent = create_agent(
            model = azure_llm_object,
            tools = [get_weather],
            system_prompt = 'You Are A Helpful Assistant.'
        )
    except Exception as error:
        return {'status': 'ERROR', 'message': str(error), 'assistant_message': 'No Response Generated', 'input_tokens': 0, 'output_tokens': 0}

    # Generate LLM Response:S4
    try:
        llm_response = llm_agent.invoke(
            {'messages': [HumanMessage(content = user_message)]}
        )
        assistant_response = llm_response["messages"][-1].content
        last_message = llm_response["messages"][-1]
        if hasattr(last_message, 'usage_metadata') and last_message.usage_metadata:
            usage = last_message.usage_metadata
            input_tokens = usage.get('input_tokens', 0) if isinstance(usage, dict) else getattr(usage, 'input_tokens', 0)
            output_tokens = usage.get('output_tokens', 0) if isinstance(usage, dict) else getattr(usage, 'output_tokens', 0)
    except Exception as error:
        return {'status': 'ERROR', 'message': str(error), 'assistant_message': 'No Response Generated', 'input_tokens': 0, 'output_tokens': 0}

    # Insert Reponse Into Database:S5
    try:
        insert_conversation(
            db_file_path = db_file_path,
            user_question_text = user_message,
            llm_answer_text = assistant_response,
            input_token = input_tokens,
            output_token = output_tokens
        )
    except Exception as error:
        return {'status': 'ERROR', 'message': str(error), 'assistant_message': 'No Response Generated', 'input_tokens': 0, 'output_tokens': 0}

    # Sending Final Message To Main Function
    return {'status': 'SUCCESS', 'message': 'Success', 'assistant_message': assistant_response, 'input_tokens': input_tokens, 'output_tokens': output_tokens}