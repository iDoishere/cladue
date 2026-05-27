# idoClaude — Claude Code Guidelines

## Project Overview

AI-powered portfolio assistant for Ido Cohen. Users chat with an AI agent that answers questions about Ido's projects, skills, experience, and contact info.

**Stack:** Vue 3 + TypeScript (frontend) · FastAPI + Agno + Gemini (backend) · ChromaDB (vector search)

---

## Common Commands

```bash
# Backend (always use venv)
cd backend
source venv/bin/activate
python3 -m uvicorn main:app --reload   # dev server → localhost:8000
python3 vector_db/index_data.py        # re-index ALL knowledge into ChromaDB (projects + skills + experience)

# Frontend
cd frontend
npm run dev                            # dev server → localhost:5173
npm run build                          # production build

# AgentOS Playground (separate server for debugging)
cd backend && python playground.py     # → connect at https://os.agno.com, endpoint http://localhost:7777

# Quick start (backend)
bash backend/start.sh
```

---

## Project Structure

```
idoClaude/
├── frontend/          # Vue 3 + Vite + TypeScript
└── backend/
    ├── main.py            # API layer — FastAPI routes only
    ├── agent.py           # Agent factory + tool registration boundary
    ├── services/          # AgentService (framework abstraction)
    ├── tools/             # Pure Python tool functions (no agno imports)
    ├── knowledge/         # Pydantic models + portfolio data
    └── vector_db/         # ChromaDB + EmbeddingProvider protocol
```

---

## Backend Architecture — Critical Rules

### 1. Tools are pure Python
Tool files in `backend/tools/` must **never** import from `agno` or any AI framework. They are plain Python functions. The `@tool` decorator is applied **only** in `agent.py`.

```python
# WRONG — never do this in tool files
from agno.tools import tool
@tool
def search_projects(...): ...

# CORRECT — pure Python in tool files
def search_projects(...): ...
# Then in agent.py: search_projects = tool(_search_projects)
```

### 2. main.py knows nothing about Agno
The API layer must only call `agent_service.chat(message, session_id)`. It must never import from `agno`, call `.run()`, or access `.content` directly.

### 3. Never use the global singleton pattern for the agent
Always use `create_agent()` from `agent.py`. Never write `portfolio_agent = Agent(...)` at module level.

### 4. Knowledge data uses Pydantic models
All data in `knowledge/` must use `Project`, `Skill`, `Experience` models from `knowledge/models.py`. Never use raw dicts. Access fields via attributes (`project.technologies`) not dict keys (`project['technologies']`).

### 5. Adding a new tool — correct process
1. Create the function in the appropriate file in `tools/` (pure Python, no agno)
2. Export it from `tools/__init__.py`
3. Import it in `agent.py` with `_` prefix and wrap with `tool()`
4. Add it to the `tools=[...]` list inside `create_agent()`

### 7. All knowledge lives in ChromaDB
All portfolio data (projects, skills, experience) is indexed into a single ChromaDB collection `portfolio_knowledge`. The agent uses `search_portfolio` for all data queries — no hardcoded Python lookups. After editing any file in `knowledge/`, re-run `python3 vector_db/index_data.py`.

### 8. Current tools (4 total)
- `search_portfolio` — semantic RAG search across all knowledge (projects, skills, experience)
- `send_contact_email` — action tool, sends email via Resend API
- `get_contact_information` — returns exact contact details (email, phone, LinkedIn)
- `get_hiring_availability` — returns structured availability answer

### 6. Swapping the embedding provider
Add a new class in `vector_db/providers.py` implementing the `EmbeddingProvider` protocol (one method: `.embed(text) -> List[float]`). Change `get_default_provider()` to return it. Nothing else changes.

---

## Environment

```bash
# backend/.env (required)
GOOGLE_API_KEY=your_key_here   # Gemini LLM + embeddings
FRONTEND_URL=http://localhost:5173   # CORS origin
```

Never commit `.env`. Use `.env.example` as the template.

---

## Key Files to Know

| File | Purpose |
|------|---------|
| `backend/main.py` | FastAPI routes — thin API layer |
| `backend/agent.py` | Agent factory, tool registration, system prompt |
| `backend/services/agent_service.py` | Agno abstraction — only file that knows agno's API |
| `backend/tools/*.py` | Pure Python business logic |
| `backend/knowledge/models.py` | Pydantic models — source of truth for data shapes |
| `backend/vector_db/providers.py` | EmbeddingProvider protocol + implementations |
| `ARCHITECTURE.md` | Full system architecture documentation |

---

## What NOT to Do

- Do not add `from agno.tools import tool` to any file except `agent.py`
- Do not access knowledge data as dicts (`project['title']`) — use attributes (`project.title`)
- Do not create a module-level `Agent(...)` instance — always use `create_agent()`
- Do not add business logic to `main.py` — it is an HTTP interface only
- Do not commit `.env` or API keys
- Do not run `pip install` outside the `venv` — always `source venv/bin/activate` first
- Do not re-index ChromaDB unless knowledge data has changed (`python3 vector_db/index_data.py`)

---

## Adding New Portfolio Data

All data lives in `backend/knowledge/`. To add a new project:

```python
# backend/knowledge/projects.py
Project(
    id="new-project",
    title="My New Project",
    description="...",
    technologies=["Vue.js", "Node.js"],
    features=["Feature 1", "Feature 2"],
    year=2025,
)
```

After adding, re-index for semantic search:
```bash
cd backend && source venv/bin/activate && python3 vector_db/index_data.py
```

---

## Testing

> ⚠️ No pytest suite yet. For medium/large tasks, run smoke tests below before committing.

### Backend smoke tests
```bash
cd backend && source venv/bin/activate

# 1. Verify imports
python3 -c "from knowledge import projects_data; print('OK')"
python3 -c "from tools import search_portfolio; print(search_portfolio('Vue skills'))"
python3 -c "from agent import create_agent; a = create_agent(); print('tools:', [t.name for t in a.tools])"

# 2. Re-index if knowledge data changed
python3 vector_db/index_data.py

# 3. Start server and test endpoints
python3 -m uvicorn main:app --reload &
sleep 4
curl -s http://localhost:8000/api/health
curl -s -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "what are Idos skills?"}'
kill %1
```

### Frontend smoke test
```bash
cd frontend && npm run dev &
sleep 6
curl -s -o /dev/null -w "%{http_code}" http://localhost:5173
kill %1
```
