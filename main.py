# Define Main Function
if __name__ == '__main__':
    # Importing Python Module:S1
    try:
        from pathlib import Path
        import os
        from dotenv import load_dotenv
        from langchain_openai import AzureChatOpenAI
        from langchain.agents import create_agent
        from langchain_core.messages import HumanMessage
        from pydantic import SecretStr
    except Exception as error:
        print(f'ERROR - [Main:S1] - {str(error)}')

    # Importing User Tools:S2
    try:
        from tools.getweathertool import get_weather
    except Exception as error:
        print(f'ERROR - [Main:S2] - {str(error)}')

    # Define Folder & File Path:S3
    try:
        parent_folder_path = Path.cwd()
        env_file_path = parent_folder_path / '.env'
    except Exception as error:
        print(f'ERROR - [Main:S3] - {str(error)}')

    # Loading Environment Variable Into Project:S4
    try:
        load_dotenv(dotenv_path=env_file_path)
        azure_api_endpoint = os.getenv('API_ENDPOINT')
        azure_api_key = os.getenv('API_KEY')
        azure_api_version = os.getenv('API_VERSION')
        azure_model_name = os.getenv('CHAT_MODEL_NAME')
    except Exception as error:
        print(f'ERROR - [Main:S4] - {str(error)}')

    # Create Azure OpenAI LLM Object:S5
    try:
        azure_llm_object = AzureChatOpenAI(
            azure_endpoint = azure_api_endpoint,
            api_key = SecretStr(azure_api_key) if azure_api_key else None,
            api_version = azure_api_version,
            azure_deployment = azure_model_name,
            temperature = 0
        )
    except Exception as error:
        print(f'ERROR - [Main:S5] - {str(error)}')

    # Create Agent With Azure OpenAI For Workflow:S6
    try:
        llm_agent = create_agent(
            model = azure_llm_object,
            tools = [get_weather],
            system_prompt = 'you are a helpful assistant.'
        )
    except Exception as error:
        print(f'ERROR - [Main:S6] - {str(error)}')

    # Calling Agent:S7
    try:
        llm_response = llm_agent.invoke(
            {'messages': [HumanMessage(content = 'What is the weather like in New York city?')]}  # type: ignore[arg-type]
        )
        # print(llm_response['messages'])
        print(f'Response:{llm_response["messages"][-1].content} [I:{(getattr(llm_response["messages"][-1], "usage_metadata", None) or {}).get("input_tokens", "N/A")}, O:{(getattr(llm_response["messages"][-1], "usage_metadata", None) or {}).get("output_tokens", "N/A")}]')
    except Exception as error:
        print(f'ERROR - [Main:S7] - {str(error)}')