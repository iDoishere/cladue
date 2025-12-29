# Ido Portfolio Backend - Agno AI Agent

Python backend using Agno framework to power intelligent AI conversations about Ido Cohen's portfolio.

## Features

- 🤖 **AI Agent** powered by Claude Sonnet 4.5
- 💾 **Conversation Memory** using SQLite
- 🔧 **Agent Tools** for searching projects and skills
- 📚 **Knowledge Base** with CV data
- 🚀 **FastAPI** REST API

## Prerequisites

- Python 3.10+
- Anthropic API key (get from https://console.anthropic.com/)

## Setup

### 1. Create virtual environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the `backend/` directory:

```bash
cp .env.example .env
```

Edit `.env` and add your Anthropic API key:

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
FRONTEND_URL=http://localhost:5176
```

## Running the Backend

### Start the server

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at:
- **API:** http://localhost:8000
- **Docs:** http://localhost:8000/docs
- **Health:** http://localhost:8000/api/health

## Project Structure

```
backend/
├── main.py              # FastAPI app entry point
├── agent.py             # Agno agent configuration
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
├── knowledge/           # CV data
│   ├── experience.py
│   ├── projects.py
│   └── skills.py
├── tools/               # Agent tools
│   ├── search_projects.py
│   ├── get_skills.py
│   └── __init__.py
└── storage/             # Session database
    └── sessions.db      # Auto-created
```

## API Endpoints

### POST /api/chat

Chat with the AI agent.

**Request:**
```json
{
  "message": "Tell me about Ido's projects",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "response": "Ido has built two impressive projects...",
  "session_id": "session-uuid"
}
```

### GET /api/health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "agent": "ready",
  "model": "claude-sonnet-4-5"
}
```

## Testing

Test the API using curl:

```bash
# Health check
curl http://localhost:8000/api/health

# Chat
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are Ido'\''s skills?"}'
```

Or visit http://localhost:8000/docs for interactive API documentation.

## Troubleshooting

### ModuleNotFoundError

Make sure you're in the virtual environment and have installed dependencies:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### CORS errors

The backend is configured to allow requests from `http://localhost:5176`. If your frontend runs on a different port, update `FRONTEND_URL` in `.env`.

### API key errors

Make sure your `.env` file contains a valid Anthropic API key:

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

## Next Steps

1. Start the backend: `python main.py`
2. Update frontend to call this API (see `frontend/src/services/ai.service.ts`)
3. Test the chat functionality
4. Deploy to Railway/Render when ready

## Cost Estimates

- **Claude API:** ~$0.003 per request
- **Estimated monthly cost:** $3-5 for typical portfolio traffic
