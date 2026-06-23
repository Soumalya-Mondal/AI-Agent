# Import Python Modules:S1
try:
    from flask import Flask, request, jsonify, render_template
    from pathlib import Path
    import os
except Exception as error:
    print(f'ERROR - [Main:S1] - {str(error)}')

# Import Define Functions:S2
try:
    from tools.llmresponse import get_llm_response
except Exception as error:
    print(f'ERROR - [Main:S2] - {str(error)}')

# Import Database Module:S3
try:
    from database.initdb import init_db
except Exception as error:
    print(f'ERROR - [Main:S3] - {str(error)}')

# Define Flask Object:S4
try:
    app = Flask(__name__, template_folder='frontend', static_folder='frontend/static', static_url_path='/static')
except Exception as error:
    print(f'ERROR - [Main:S4] - {str(error)}')

# Define Folder And File Path:S5
try:
    parent_folder_path = Path.cwd()
    database_folder_path = parent_folder_path / 'database'
    database_file_path = database_folder_path / 'chat_conversations.db'
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

        if not user_message:
            return jsonify({
                'error': 'Message Cannot Be Empty'
            }), 400

        assistant_response, input_tokens, output_tokens = get_llm_response(
            user_message, str(database_file_path)
        )

        return jsonify({
            'response': assistant_response,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens
        }), 200
    except Exception as error:
        print(f'ERROR - [Main:S7] - {str(error)}')
        return jsonify({
            'error': 'Failed To Generate Response'
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
