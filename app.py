# Import Python Modules:S1
try:
    from flask import Flask, request, jsonify, render_template
    from pathlib import Path
    import os
    from dotenv import load_dotenv
    from langchain_openai import AzureChatOpenAI
    from langchain.agents import create_agent
    from langchain_core.messages import HumanMessage
    from pydantic import SecretStr
except Exception as error:
    print(f'ERROR - [Main:S1] - {str(error)}')

# Import Define Functions:S2
try:
    from tools.getweathertool import get_weather
except Exception as error:
    print(f'ERROR - [Main:S2] - {str(error)}')

# Import Database Module:S2.1
try:
    from database.initdb import init_db
    from database.dbdatainsert import insert_conversation
except Exception as error:
    print(f'ERROR - [Main:S2.1] - {str(error)}')

# Define Flask Object:S3
try:
    app = Flask(__name__, template_folder = 'frontend', static_folder = 'frontend/static', static_url_path = '/static')
except Exception as error:
    print(f'ERROR - [Main:S3] - {str(error)}')

# Define Folder And File Path:S4
try:
    parent_folder_path = Path.cwd()
    env_file_path = parent_folder_path / '.env'
    database_folder_path = parent_folder_path / 'database'
    database_file_path = database_folder_path / 'chat_conversations.db'
except Exception as error:
    print(f'ERROR - [Main:S4] - {str(error)}')

# Loading Environment Variables:S5
try:
    load_dotenv(dotenv_path = env_file_path)
    azure_api_endpoint = os.getenv('API_ENDPOINT')
    azure_api_key = os.getenv('API_KEY')
    azure_api_version = os.getenv('API_VERSION')
    azure_model_name = os.getenv('CHAT_MODEL_NAME')
except Exception as error:
    print(f'ERROR - [Main:S5] - {str(error)}')

# Create Azure OpenAI LLM Object:S6
try:
    azure_llm_object = AzureChatOpenAI(
        azure_endpoint = azure_api_endpoint,
        api_key = SecretStr(azure_api_key) if azure_api_key else None,
        api_version = azure_api_version,
        azure_deployment = azure_model_name,
        temperature = 0
    )
except Exception as error:
    print(f'ERROR - [Main:S6] - {str(error)}')

# Create Agent With Azure OpenAI For Workflow:S7
try:
    llm_agent = create_agent(
        model = azure_llm_object,
        tools = [get_weather],
        system_prompt = 'You Are A Helpful Assistant.'
    )
except Exception as error:
    print(f'ERROR - [Main:S7] - {str(error)}')

# Initialize Database:S8
try:
    if not database_file_path.exists():
        init_db(str(database_file_path))
except Exception as error:
    print(f'ERROR - [Main:S8] - {str(error)}')

# Route to serve the chat interface
@app.route('/')
def index():
    return render_template('index.html')

# API Route to handle chat messages
@app.route('/api/chat', methods = ['POST'])
def chat():
    # Fetch User Message From Request and Call Agent to Generate Response:S9
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({
                'error': 'Message Cannot Be Empty'
            }), 400

        # Calling Agent with user message:S10
        try:
            llm_response = llm_agent.invoke(
                {'messages': [HumanMessage(content = user_message)]} # type: ignore[arg-type]
            )
            assistant_response = llm_response["messages"][-1].content
            # Define Intial Constant
            input_tokens = 0
            output_tokens = 0

            # Extract token usage information:S11
            try:
                # Get usage info from the last message in the response
                last_message = llm_response["messages"][-1]
                # Extract from usage_metadata
                if hasattr(last_message, 'usage_metadata') and last_message.usage_metadata:
                    usage = last_message.usage_metadata
                    input_tokens = usage.get('input_tokens', 0) if isinstance(usage, dict) else getattr(usage, 'input_tokens', 0)
                    output_tokens = usage.get('output_tokens', 0) if isinstance(usage, dict) else getattr(usage, 'output_tokens', 0)
            except Exception as error:
                print(f'ERROR - [Main:S11] - Failed To Extract Token Usage: {str(error)}')

            # Insert conversation record into database:S12
            try:
                insert_conversation(
                    db_file_path=str(database_file_path),
                    user_question_text=user_message,
                    llm_answer_text=assistant_response,
                    input_token=input_tokens,
                    output_token=output_tokens
                )
            except Exception as error:
                print(f'ERROR - [Main:S12] - {str(error)}')

            return jsonify({
                'response': assistant_response,
                'input_tokens': input_tokens,
                'output_tokens': output_tokens
            }), 200
        except Exception as error:
            print(f'ERROR - [Main:S10] - {str(error)}')
            return jsonify({
                'error': 'Failed To Generate Response'
            }), 500
    except Exception as error:
        print(f'ERROR - [Main:S9] - {str(error)}')
        return jsonify({
            'error': str(error)
        }), 400

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)