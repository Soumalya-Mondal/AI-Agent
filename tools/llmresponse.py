# Define "get_llm_response" Function
def get_llm_response(user_message: str, db_file_path: str) -> tuple:
    # Import Python Modules:S1
    try:
        from pathlib import Path
        import os
        from dotenv import load_dotenv
        from langchain_openai import AzureChatOpenAI
        from langchain.agents import create_agent
        from langchain_core.messages import HumanMessage
        from pydantic import SecretStr
        from tools.getweathertool import get_weather
        from database.dbdatainsert import insert_conversation
    except Exception as error:
        print(f'ERROR - [LLM-Response:S1] - {str(error)}')

    # Define Folder Paths and File Paths:S2
    try:
        parent_folder_path = Path.cwd()
        env_file_path = parent_folder_path / '.env'
    except Exception as error:
        print(f'ERROR - [LLM-Response:S2] - {str(error)}')

    # Loading Environment Variables:S3
    try:
        load_dotenv(dotenv_path=env_file_path)
        azure_api_endpoint = os.getenv('API_ENDPOINT')
        azure_api_key = os.getenv('API_KEY')
        azure_api_version = os.getenv('API_VERSION')
        azure_model_name = os.getenv('CHAT_MODEL_NAME')
    except Exception as error:
        print(f'ERROR - [LLM-Response:S3] - {str(error)}')

    # Create Azure OpenAI LLM Object:S4
    try:
        azure_llm_object = AzureChatOpenAI(
            azure_endpoint=azure_api_endpoint,
            api_key=SecretStr(azure_api_key) if azure_api_key else None,
            api_version=azure_api_version,
            azure_deployment=azure_model_name,
            temperature=0
        )
    except Exception as error:
        print(f'ERROR - [LLM-Response:S4] - {str(error)}')

    # Create Agent With Azure OpenAI For Workflow:S5
    try:
        llm_agent = create_agent(
            model=azure_llm_object,
            tools=[get_weather],
            system_prompt='You Are A Helpful Assistant.'
        )
    except Exception as error:
        print(f'ERROR - [LLM-Response:S5] - {str(error)}')

    # Calling Agent with user message:S6
    try:
        llm_response = llm_agent.invoke(
            {'messages': [HumanMessage(content=user_message)]} # type: ignore[arg-type]
        )
        assistant_response = llm_response["messages"][-1].content
        # Define Initial Constant
        input_tokens = 0
        output_tokens = 0

        # Extract token usage information:S7
        try:
            last_message = llm_response["messages"][-1]
            if hasattr(last_message, 'usage_metadata') and last_message.usage_metadata:
                usage = last_message.usage_metadata
                input_tokens = usage.get('input_tokens', 0) if isinstance(usage, dict) else getattr(usage, 'input_tokens', 0)
                output_tokens = usage.get('output_tokens', 0) if isinstance(usage, dict) else getattr(usage, 'output_tokens', 0)
        except Exception as error:
            print(f'ERROR - [LLM-Response:S7] - Failed To Extract Token Usage: {str(error)}')

        # Insert conversation record into database:S8
        try:
            insert_conversation(
                db_file_path=db_file_path,
                user_question_text=user_message,
                llm_answer_text=assistant_response,
                input_token=input_tokens,
                output_token=output_tokens
            )
        except Exception as error:
            print(f'ERROR - [LLM-Response:S8] - {str(error)}')

        # Return Final Message To Main Function
        return assistant_response, input_tokens, output_tokens
    except Exception as error:
        print(f'ERROR - [LLM-Response:S6] - {str(error)}')
        raise