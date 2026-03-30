# ido — AI Portfolio Assistant

An AI-powered portfolio where recruiters can chat with an intelligent assistant to learn about Ido Cohen's experience, projects, and skills — and send him a message directly through the chat.

**Live:** [cladue-production.up.railway.app](https://cladue-production.up.railway.app)

---

## What it does

- **Chat with AI** — ask anything about Ido's experience, projects, or skills
- **RAG-powered answers** — all portfolio data lives in ChromaDB, retrieved semantically via embeddings
- **Send email** — the agent collects your info and sends Ido a message via Resend API
- **Session memory** — conversation context is preserved across messages

---

## Tech Stack

**Frontend**
- Vue 3 + TypeScript + Vite
- Component architecture with composables
- Aurora background, cursor trail, onboarding modal

**Backend**
- FastAPI (Python)
- Agno — AI agent framework
- Gemini 2.5 Flash — LLM + embeddings
- ChromaDB — vector database for semantic search (RAG)
- SQLite — session/conversation memory
- Resend — email delivery

**Infrastructure**
- Docker (multi-stage build)
- Railway — deployment & hosting

---

## Architecture

```
User → Vue 3 frontend → FastAPI → Agno Agent → Gemini LLM
                                       ↓
                              ChromaDB (RAG search)
                              SQLite (session memory)
                              Resend (email)
```

The agent has 4 tools:

| Tool | Purpose |
|------|---------|
| `search_portfolio` | Semantic RAG search across all knowledge |
| `get_contact_information` | Returns email, phone, LinkedIn |
| `get_hiring_availability` | Returns availability status |
| `send_contact_email` | Sends email via Resend API |

---

## Run locally

**Backend**
```bash
cd backend
source venv/bin/activate
cp .env.example .env        # add your GOOGLE_API_KEY
python3 -m uvicorn main:app --reload
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

---

## Environment Variables

```bash
# backend/.env
GOOGLE_API_KEY=your_gemini_key
RESEND_API_KEY=your_resend_key
FRONTEND_URL=http://localhost:5173
```

---

Built by [Ido Cohen](https://github.com/iDoishere)