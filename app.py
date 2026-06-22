# Importing Python Module:S1
from flask import Flask, request, jsonify, render_template
from pathlib import Path
import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from pydantic import SecretStr
from tools.getweathertool import get_weather

# Define Flask Object:S2
app = Flask(__name__, template_folder='frontend', static_folder='frontend/static', static_url_path='/static')

# Loading Environment Variables:S3
try:
    parent_folder_path = Path.cwd()
    env_file_path = parent_folder_path / '.env'
    load_dotenv(dotenv_path=env_file_path)
    azure_api_endpoint = os.getenv('API_ENDPOINT')
    azure_api_key = os.getenv('API_KEY')
    azure_api_version = os.getenv('API_VERSION')
    azure_model_name = os.getenv('CHAT_MODEL_NAME')
except Exception as error:
    print(f'ERROR - [Main:S3] - {str(error)}')

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
    print(f'ERROR - [Main:S4] - {str(error)}')

# Create Agent With Azure OpenAI For Workflow:S5
try:
    llm_agent = create_agent(
        model=azure_llm_object,
        tools=[get_weather],
        system_prompt='you are a helpful assistant.'
    )
except Exception as error:
    print(f'ERROR - [Main:S5] - {str(error)}')


# Route to serve the chat interface
@app.route('/')
def index():
    """Serve the main chat interface"""
    return render_template('index.html')


# API Route to handle chat messages
@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle chat messages from the frontend.
    Expects JSON: {"message": "user message"}
    Returns JSON: {"response": "assistant response"}
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Calling Agent with user message:S6
        try:
            llm_response = llm_agent.invoke(
                {'messages': [HumanMessage(content=user_message)]}  # type: ignore[arg-type]
            )
            assistant_response = llm_response["messages"][-1].content
            
            # Extract token usage information:S6a
            input_tokens = 0
            output_tokens = 0
            
            try:
                # Try to get usage info from the response
                if hasattr(llm_response, 'usage_metadata') and llm_response.usage_metadata:
                    input_tokens = llm_response.usage_metadata.get('input_tokens', 0)
                    output_tokens = llm_response.usage_metadata.get('output_tokens', 0)
                elif 'usage_metadata' in llm_response:
                    input_tokens = llm_response['usage_metadata'].get('input_tokens', 0)
                    output_tokens = llm_response['usage_metadata'].get('output_tokens', 0)
            except Exception as token_error:
                print(f'WARNING - [Main:S6a] - Could not extract token usage: {str(token_error)}')
            
            return jsonify({
                'response': assistant_response,
                'input_tokens': input_tokens,
                'output_tokens': output_tokens
            }), 200
        except Exception as agent_error:
            print(f'ERROR - [Main:S6] - {str(agent_error)}')
            return jsonify({'error': 'Failed to generate response'}), 500
    
    except Exception as error:
        print(f'ERROR - [Main:S6] - {str(error)}')
        return jsonify({'error': str(error)}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)