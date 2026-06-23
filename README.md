# AI Agent - Intelligent Chat Application

A modern, intelligent chatbot application powered by Azure OpenAI LLM with integrated weather tool capabilities. This project combines Flask backend, LangChain orchestration, and SQLite persistence to deliver an interactive AI-driven conversational experience.

## Overview

This AI Agent application provides a chat interface where users can interact with an intelligent assistant that:
- Responds to natural language queries with context-aware answers
- Accesses real-time weather information via OpenWeatherMap API
- Tracks conversation history with token usage analytics
- Maintains persistent conversation logs in a local SQLite database

## Technology Stack

- **Backend Framework**: Flask 3.0.0+
- **AI/LLM**: Azure OpenAI with LangChain
- **Language Model**: LangChain (LangChain OpenAI integration)
- **Agent Framework**: LangChain Agents with Tool Integration
- **Database**: SQLite3
- **API Integration**: OpenWeatherMap API
- **Environment Management**: Python-dotenv
- **Python Version**: 3.12+

## Project Structure

```
AI-Agent/
├── app.py                 # Main Flask application & routing
├── frontend/              # Web interface (HTML/CSS/JS)
│   ├── index.html
│   └── static/
├── tools/                 # Custom agent tools
│   ├── llmresponse.py     # LLM agent orchestration & response generation
│   └── getweathertool.py  # Real-time weather data retrieval
├── database/              # Data persistence layer
│   ├── initdb.py          # Database initialization & schema
│   └── dbdatainsert.py    # Conversation logging
├── .env                   # Environment configuration (not in repo)
├── pyproject.toml         # Python package dependencies
└── README.md              # This file
```

## Features

### 1. **Intelligent Chat Interface**
- Real-time conversation with Azure OpenAI LLM
- Token usage tracking (input/output)
- Natural language processing with context awareness

### 2. **Weather Tool Integration**
- Query current weather conditions for any city worldwide
- Automatic geographic coordinate resolution
- Real-time data from OpenWeatherMap API
- Fallback error handling for unavailable cities

### 3. **Conversation Persistence**
- Automatic logging of all conversations to SQLite database
- Tracked metrics: user queries, AI responses, token usage
- Historical conversation records for audit & analytics

### 4. **Web Interface**
- Clean, responsive HTML/CSS frontend
- RESTful API integration
- Real-time response streaming

## Installation

### Prerequisites
- Python 3.12 or higher
- Azure OpenAI API credentials
- OpenWeatherMap API key

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI-Agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   # or using uv (if available)
   uv pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create a `.env` file in the project root:
   ```env
   API_ENDPOINT=https://<your-azure-region>.openai.azure.com/
   API_KEY=<your-azure-openai-api-key>
   API_VERSION=2024-08-01-preview
   CHAT_MODEL_NAME=<your-deployment-name>
   OPEN_WEATHER_API_KEY=<your-openweather-api-key>
   ```

4. **Run the application**
   ```bash
   python app.py
   ```
   The application will be available at `http://localhost:5000`

## API Endpoints

### `GET /`
Serves the chat interface (index.html)

### `POST /api/chat`
Handles user messages and returns AI responses

**Request Body:**
```json
{
  "message": "What is the weather like in London?"
}
```

**Response (200 OK):**
```json
{
  "response": "The weather in London is clear sky, 15°C (feels like 13°C), humidity 72%.",
  "input_tokens": 45,
  "output_tokens": 28
}
```

**Error Response (400/500):**
```json
{
  "error": "Message Cannot Be Empty"
}
```

## Module Documentation

### `app.py` - Main Application
- Flask application initialization
- Route definitions for web interface and API
- Database initialization on startup
- Error handling and logging

### `tools/llmresponse.py` - LLM Agent Orchestration
- Creates Azure OpenAI LLM instance with zero temperature (deterministic responses)
- Initializes LangChain agent with available tools
- Handles agent invocation and response processing
- Extracts token usage metrics from responses
- Persists conversations to database

### `tools/getweathertool.py` - Weather Tool
- Queries OpenWeatherMap Geocoding API for city coordinates
- Fetches real-time weather data (temperature, humidity, conditions)
- Handles city resolution and API failures gracefully
- Returns human-readable weather summaries

### `database/initdb.py` - Database Initialization
- Creates SQLite connection
- Defines `conversations` table schema with auto-increment primary key
- Ensures idempotent table creation

### `database/dbdatainsert.py` - Data Persistence
- Inserts conversation records into database
- Stores: user question, LLM response, token counts
- Handles connection lifecycle management

## Database Schema

### `conversations` Table
```sql
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_question_text TEXT NOT NULL,
    llm_answer_text TEXT NOT NULL,
    input_token INT NOT NULL,
    output_token INT NOT NULL
)
```

## Configuration

### Environment Variables
| Variable | Description | Example |
|----------|-------------|---------|
| `API_ENDPOINT` | Azure OpenAI endpoint URL | `https://eastus.openai.azure.com/` |
| `API_KEY` | Azure OpenAI API key | (sensitive, keep secret) |
| `API_VERSION` | Azure OpenAI API version | `2024-08-01-preview` |
| `CHAT_MODEL_NAME` | Deployment model name | `gpt-4-turbo` |
| `OPEN_WEATHER_API_KEY` | OpenWeatherMap API key | (sensitive, keep secret) |

### Flask Configuration
- **Debug Mode**: Enabled (development)
- **Host**: `0.0.0.0` (accessible from any interface)
- **Port**: `5000`
- **Frontend Folder**: `frontend/`
- **Static Files**: `frontend/static/`

## Usage Examples

### Example 1: Simple Question
```
User: "What is 2+2?"
Agent: "2+2 equals 4."
```

### Example 2: Weather Query
```
User: "What's the weather in Paris?"
Agent: "The weather in Paris is light rain, 12°C (feels like 10°C, min 10°C, max 14°C), humidity 85%."
```

### Example 3: Complex Query
```
User: "I'm traveling to Tokyo next week. What should I pack based on the weather?"
Agent: [Uses weather tool to fetch Tokyo conditions, then provides packing recommendations]
```

## Error Handling

The application includes comprehensive error handling:
- **Empty Messages**: Returns 400 error with "Message Cannot Be Empty"
- **LLM Failures**: Returns 500 error with "Failed To Generate Response"
- **Weather Unavailable**: Gracefully returns error message without failing entire request
- **Database Errors**: Logged but don't interrupt conversation flow
- **Token Extraction**: Safe fallback to 0 tokens if metadata unavailable

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| langchain | >=1.3.10 | LLM orchestration framework |
| langchain-community | >=0.4.2 | Community integrations |
| langchain-openai | >=1.3.2 | Azure OpenAI integration |
| python-dotenv | >=1.2.2 | Environment variable management |
| flask | >=3.0.0 | Web framework |

See `pyproject.toml` for complete dependency list.

## Performance Considerations

- **LLM Temperature**: Set to 0 for deterministic, consistent responses
- **Token Tracking**: All conversations tracked for cost & performance monitoring
- **Database**: SQLite optimized for local development; consider PostgreSQL for production
- **Concurrency**: Flask development server; use Gunicorn/uWSGI for production

## Security Notes

⚠️ **Important**:
- Never commit `.env` file with API keys to version control
- Use environment variables or secrets management in production
- Validate user input before sending to LLM
- Implement rate limiting on `/api/chat` endpoint for production
- Use HTTPS in production environments
- Store sensitive API keys in secure vaults (Azure Key Vault, etc.)

## Development

### Running in Development Mode
```bash
python app.py
```

### Cleaning Cache
```bash
# On Linux/Mac
./CleanCache.sh

# On Windows
.\CleanCache.ps1
```

### Project Metadata
- **Name**: ai-agent
- **Version**: 0.1.0
- **Python**: >=3.12
- **License**: (Specify your license)

## Future Enhancements

- [ ] Multiple conversation sessions/threading
- [ ] Conversation export (PDF, JSON)
- [ ] Advanced tool integration (web search, calculations, etc.)
- [ ] User authentication & multi-user support
- [ ] Production database migration (PostgreSQL/MongoDB)
- [ ] Rate limiting and API throttling
- [ ] Monitoring and logging dashboard
- [ ] Prompt optimization and fine-tuning
- [ ] Multi-language support
- [ ] Voice input/output capabilities

## Troubleshooting

### Issue: "Message Cannot Be Empty"
- Ensure POST request includes a `message` field
- Check that message is not just whitespace

### Issue: "Failed To Generate Response"
- Verify Azure OpenAI credentials in `.env`
- Check API endpoint and deployment name
- Ensure network connectivity to Azure services

### Issue: Weather Tool Returns Errors
- Validate OpenWeatherMap API key
- Check if city name is correctly spelled
- Verify API rate limits haven't been exceeded

### Issue: Database Errors
- Ensure `database/` folder exists and is writable
- Check file permissions on `chat_conversations.db`
- Verify SQLite3 is installed

## Contributing

(Add contribution guidelines here)

## License

(Specify your license here - e.g., MIT, Apache 2.0, etc.)

## Contact & Support

For issues, questions, or feedback, please contact [your contact information].

---

**Last Updated**: June 2026  
**Version**: 0.1.0
