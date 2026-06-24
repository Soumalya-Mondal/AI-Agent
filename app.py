# Import Python Modules:S1
try:
    from flask import Flask, request, jsonify, render_template
    from pathlib import Path
    from dotenv import load_dotenv
except Exception as error:
    print(f'ERROR - [Main:S1] - {str(error)}')

# Import Modules:S2
try:
    from tools.llmresponse import get_llm_response
    from database.initdb import init_db
except Exception as error:
    print(f'ERROR - [Main:S2] - {str(error)}')

# Define Flask Object:S3
try:
    app = Flask(__name__, template_folder='frontend', static_folder='frontend/static', static_url_path='/static')
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

# Load Environment Variables at OS Level:S5
try:
    load_dotenv(dotenv_path = env_file_path)
except Exception as error:
    print(f'ERROR - [Main:S5] - {str(error)}')

# Initialize Database:S6
try:
    if not database_file_path.exists():
        init_db(str(database_file_path))
except Exception as error:
    print(f'ERROR - [Main:S6] - {str(error)}')


# Route to serve the chat interface
@app.route('/')
def index():
    return render_template('index.html')

# API Route to handle chat messages
@app.route('/api/chat', methods=['POST'])
def chat():
    # Fetch User Message From Request and Call Agent to Generate Response:S7
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()

        # Check If The User Message Is Not Empty
        if not user_message:
            return jsonify({
                'error': 'Message Cannot Be Empty'
            }), 400

        # Calling "get_llm_response" Function For Answer Generation
        llm_response_result = get_llm_response(user_message = user_message, db_file_path = str(database_file_path))

        if (llm_response_result['status'] == 'SUCCESS'):
            return jsonify({
                'response': llm_response_result['assistant_message'],
                'input_tokens': llm_response_result['input_tokens'],
                'output_tokens': llm_response_result['output_tokens']
            }), 200
        else:
            return jsonify({
                'error': llm_response_result['message']
            }), 500
    except Exception as error:
        print(f'ERROR - [Main:S7] - {str(error)}')
        return jsonify({
            'error': 'Failed To Generate Response'
        }), 500

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)