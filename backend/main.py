from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from services import AgentService
from agent import create_agent

agent_service = AgentService(create_agent())
import uuid
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Ido Portfolio API",
    description="AI-powered portfolio backend using Agno framework",
    version="1.0.0"
)

# Enable CORS for Vue frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:5176",
        os.getenv("FRONTEND_URL", "http://localhost:5176")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


class ChatResponse(BaseModel):
    response: str
    session_id: str


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint - processes user message and returns AI response with conversation memory.

    Args:
        request: ChatRequest containing user message and optional session_id

    Returns:
        ChatResponse with AI response and session_id
    """
    try:
        # Create or use existing session
        session_id = request.session_id or str(uuid.uuid4())

        print(f"\n{'='*50}")
        print(f"Session: {session_id}")
        print(f"User: {request.message}")
        print(f"{'='*50}\n")

        # Get AI response with conversation memory
        response_text = agent_service.chat(request.message, session_id)

        print(f"\n{'='*50}")
        print(f"Assistant: {response_text}")
        print(f"{'='*50}\n")

        return ChatResponse(
            response=response_text,
            session_id=session_id
        )

    except Exception as e:
        print(f"\nError: {str(e)}\n")
        error = str(e).lower()
        if "429" in error or "quota" in error or "rate" in error or "exhausted" in error:
            friendly = "I'm getting too many requests right now. Please try again in a moment."
        else:
            friendly = "Something went wrong on my end. Please try again."
        return ChatResponse(response=friendly, session_id=session_id)


@app.get("/api/health")
async def health():
    """Health check endpoint to verify API is running"""
    return {
        "status": "healthy",
        "agent": "ready",
        "model": "gemini-2.5-flash"
    }


# Serve Vue frontend static files (MUST be after API routes)
# In production, Docker copies Vue build to ./static
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")


if __name__ == "__main__":
    import uvicorn

    print("\n" + "="*60)
    print("🚀 Starting Ido Portfolio API (Auto-Reload Enabled)")
    print("="*60)
    print(f"📍 API: http://localhost:8000")
    print(f"📚 Docs: http://localhost:8000/docs")
    print(f"🔗 Frontend: http://localhost:5176")
    print("="*60 + "\n")

    uvicorn.run(
        "main:app",  # Changed from app to "main:app" for reload
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload
        log_level="info"
    )
