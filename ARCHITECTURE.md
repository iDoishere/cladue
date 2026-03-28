# idoClaude — System Architecture

## Overview

idoClaude is an AI-powered portfolio assistant. Visitors chat with an agent that knows everything about Ido Cohen — his projects, skills, experience, and contact details. The system consists of a **Vue 3 frontend** and a **FastAPI + Agno backend**, connected via a REST API.

---

## System Context

```
┌─────────────────────────────────────────────────────────────┐
│                         Browser                             │
│                                                             │
│   ┌─────────────────────┐      ┌──────────────────────┐    │
│   │   Vue 3 Frontend    │      │   FastAPI Backend     │    │
│   │   (Vite / TS)       │◄────►│   (Python / Agno)    │    │
│   │   localhost:5173    │      │   localhost:8000      │    │
│   └─────────────────────┘      └──────────┬───────────┘    │
│                                           │                  │
└───────────────────────────────────────────┼──────────────────┘
                                            │
                        ┌───────────────────┼──────────────────┐
                        │                  │  External APIs     │
                        │   ┌──────────────▼──────┐            │
                        │   │  Google Gemini API  │            │
                        │   │  (LLM + Embeddings) │            │
                        │   └─────────────────────┘            │
                        │   ┌─────────────────────┐            │
                        │   │  ChromaDB (local)   │            │
                        │   │  (Vector Search)    │            │
                        │   └─────────────────────┘            │
                        └─────────────────────────────────────┘
```

---

## Frontend

**Stack:** Vue 3, TypeScript, Vite, Tailwind CSS

### Responsibilities
- Renders the chat UI
- Sends `POST /api/chat` with user messages
- Displays streamed AI responses
- Manages session ID across messages (conversation memory)

### Key Files
```
frontend/
├── src/
│   ├── components/     # Vue components (chat UI, animations)
│   ├── views/          # Page-level views
│   └── main.ts         # App entry point
├── vite.config.ts      # Dev proxy → backend :8000
└── package.json
```

### Frontend → Backend Communication
The frontend sends a simple JSON payload:
```json
POST /api/chat
{
  "message": "What are Ido's Vue.js skills?",
  "session_id": "abc123"   // optional — created on first message
}
```
And receives:
```json
{
  "response": "Ido has 90% proficiency in Vue.js...",
  "session_id": "abc123"
}
```

---

## Backend

**Stack:** Python, FastAPI, Agno, Gemini 2.5 Flash, ChromaDB, Pydantic

### Architecture Overview

The backend follows a **layered architecture** with clear separation of concerns and adherence to SOLID OOP principles. Each layer has a single responsibility and communicates only with the layer directly below it.

```
┌────────────────────────────────────────────────────────────┐
│                    API Layer (main.py)                     │
│           FastAPI routes, Pydantic request/response        │
└──────────────────────────┬─────────────────────────────────┘
                           │ calls
┌──────────────────────────▼─────────────────────────────────┐
│              Service Layer (services/)                     │
│           AgentService — framework-agnostic interface      │
└──────────────────────────┬─────────────────────────────────┘
                           │ calls
┌──────────────────────────▼─────────────────────────────────┐
│              Agent Layer (agent.py)                        │
│     create_agent() factory — Agno + Gemini configuration   │
│     @tool registration boundary                            │
└──────────────────────────┬─────────────────────────────────┘
                           │ calls
┌──────────────────────────▼─────────────────────────────────┐
│               Tool Layer (tools/)                          │
│     Pure Python functions — zero framework dependencies    │
│     9 tools: search, skills, experience, contact           │
└──────────────┬───────────────────────┬─────────────────────┘
               │                       │
┌──────────────▼──────────┐  ┌────────▼────────────────────┐
│   Knowledge Layer       │  │   Vector DB Layer            │
│   (knowledge/)          │  │   (vector_db/)               │
│   Pydantic models:      │  │   ChromaDB + Embeddings      │
│   Project, Skill,       │  │   EmbeddingProvider Protocol │
│   Experience            │  │   GeminiEmbeddingProvider    │
└─────────────────────────┘  └──────────────────────────────┘
```

---

### Layer 1 — API Layer (`main.py`)

**Responsibility:** HTTP interface only. Knows nothing about AI frameworks.

```python
# main.py
agent_service = AgentService(create_agent())

@app.post("/api/chat")
async def chat(request: ChatRequest):
    response_text = agent_service.chat(request.message, session_id)
    return ChatResponse(response=response_text, session_id=session_id)
```

**What it does:**
- Defines FastAPI routes (`/api/chat`, `/api/health`)
- Validates request/response with Pydantic models
- Delegates all AI logic to `AgentService`
- Manages CORS for the Vue frontend

**What it does NOT do:**
- Know that Agno exists
- Know that Gemini is the LLM
- Handle any business logic

---

### Layer 2 — Service Layer (`services/`)

**Responsibility:** Translate between the API layer and the AI framework.

```python
# services/agent_service.py
class AgentService:
    def __init__(self, agent):
        self._agent = agent

    def chat(self, message: str, session_id: str) -> str:
        response = self._agent.run(message, session_id=session_id)
        return response.content  # agno-specific translation lives HERE only
```

**SOLID principle applied:**
- **Dependency Inversion (D):** `main.py` depends on `AgentService` (abstraction), not on agno directly
- **Single Responsibility (S):** `AgentService` has one job — translate between the API and the agent

**Why this matters:** Replacing Agno with LangChain, Claude SDK, or any other framework means editing only this file. The API layer never changes.

---

### Layer 3 — Agent Layer (`agent.py`)

**Responsibility:** AI agent configuration and tool registration boundary.

```python
# agent.py — THE boundary where agno meets business logic
from agno.tools import tool

# Pure Python tools → wrapped with agno decorator HERE, not in tool files
search_projects = tool(_search_projects)
get_skill_level = tool(_get_skill_level)
# ... all 9 tools

def create_agent() -> Agent:
    return Agent(
        model=Gemini(id="gemini-2.5-flash"),
        tools=[search_projects, get_skill_level, ...],
        instructions=[...],
    )
```

**SOLID principles applied:**
- **Single Responsibility (S):** Agent config and tool registration in one place
- **Open/Closed (O):** `create_agent()` is a factory — extend without modifying existing code
- **Dependency Inversion (D):** Tools are injected as parameters, not hardcoded

**Why factory over singleton:**
The old code had `portfolio_agent = Agent(...)` at module level — this ran on import, connected to Gemini immediately, and made testing impossible. The factory `create_agent()` creates the agent only when called, with no side effects on import.

---

### Layer 4 — Tool Layer (`tools/`)

**Responsibility:** Pure business logic functions with zero framework dependencies.

```
tools/
├── search_portfolio.py     # RAG search across ALL knowledge (projects, skills, experience)
├── get_contact_info.py     # exact contact info + hiring availability
├── send_contact_email.py   # action tool — sends email via Resend API
└── __init__.py
```

**4 tools total** — agent uses `search_portfolio` for all data questions, the other 3 for specific actions or exact lookups.

**Key design decision:** No `@tool` decorator in tool files. The decorator is applied in `agent.py`. This means:
- Tools are pure Python — testable without any AI framework installed
- Switching from Agno to LangChain = change the decorator import in `agent.py`, not in every tool file

```python
# tool file — pure Python
def search_portfolio(query, type_filter=None): ...

# agent.py wraps it:
search_portfolio = tool(_search_portfolio)
```

---

### Layer 5a — Knowledge Layer (`knowledge/`)

**Responsibility:** Typed, validated data models for Ido's portfolio data.

```
knowledge/
├── models.py        # Pydantic models: Project, Skill, Experience
├── projects.py      # 3 projects as Project instances
├── skills.py        # 17+ skills as Skill instances
├── experience.py    # 3 roles as Experience instances
└── __init__.py
```

**Pydantic models:**
```python
class Project(BaseModel):
    id: str
    title: str
    description: str
    technologies: List[str]
    features: List[str]
    year: int
    github: Optional[str] = None
    demo: Optional[str] = None

class Skill(BaseModel):
    name: str
    level: int        # 0-100
    category: str     # "frontend" | "backend" | "tools"

class Experience(BaseModel):
    title: str
    company: str
    location: str
    period: str
    current: bool
    responsibilities: List[str]
    technologies: List[str]
```

**Why Pydantic over raw dicts:**
- Typos like `project['technolgoies']` become `project.technologies` — IDE catches it immediately
- Wrong types (e.g. `year="twenty-twenty"`) raise a validation error at startup, not silently at runtime
- Full IDE autocomplete on all fields

---

### Layer 5b — Vector DB Layer (`vector_db/`)

**Responsibility:** Semantic search via embeddings and ChromaDB.

```
vector_db/
├── providers.py     # EmbeddingProvider Protocol + implementations
├── setup.py         # ChromaDB client, indexing, search functions
├── index_data.py    # Script to index projects into ChromaDB
└── __init__.py
```

#### EmbeddingProvider Protocol

```python
# providers.py
class EmbeddingProvider(Protocol):
    def embed(self, text: str) -> List[float]: ...

class GeminiEmbeddingProvider:    # production
    def embed(self, text: str) -> List[float]: ...

class NullEmbeddingProvider:      # no API key / fallback
    def embed(self, text: str) -> List[float]:
        return [0.0] * 768
```

**SOLID principles applied:**
- **Open/Closed (O):** Add `OpenAIEmbeddingProvider` without touching anything else
- **Liskov Substitution (L):** Any provider can replace any other — `setup.py` works with all of them
- **Interface Segregation (I):** Protocol has one method — minimal contract
- **Dependency Inversion (D):** `setup.py` depends on the Protocol, not on Gemini directly

#### How Semantic Search Works

```
User query: "projects with real-time features"
     │
     ▼
GeminiEmbeddingProvider.embed(query)
     │  → [0.234, -0.112, 0.891, ...]  (768-dim vector)
     ▼
ChromaDB.query(query_embeddings=[...])
     │  → nearest neighbors by cosine distance
     ▼
Enriched with full Project data from knowledge/
     │
     ▼
JSON returned to agent → formatted response to user
```

---

## Data Flow — Full Request Lifecycle

```
User types: "What Vue.js projects has Ido built?"

1. Frontend (Vue)
   └─ POST /api/chat { message, session_id }

2. API Layer (main.py)
   └─ agent_service.chat(message, session_id)

3. Service Layer (AgentService)
   └─ self._agent.run(message, session_id=session_id)

4. Agent Layer (Agno + Gemini)
   ├─ LLM decides: use search_portfolio(query="Vue projects", type_filter="project")
   └─ calls tool function

5. Tool Layer (search_portfolio)
   ├─ converts query to vector via Gemini embeddings
   ├─ searches ChromaDB (portfolio_knowledge collection)
   └─ returns matching document content

6. Agent Layer
   └─ LLM formats tool result into natural language response

7. Service Layer
   └─ returns response.content as plain str

8. API Layer
   └─ ChatResponse(response=text, session_id=session_id)

9. Frontend
   └─ displays response in chat UI
```

---

## SOLID Principles — Applied

| Principle | Where | How |
|-----------|-------|-----|
| **S** — Single Responsibility | Every layer | Each file/class has one clear job |
| **O** — Open/Closed | `EmbeddingProvider`, `create_agent()` | Add new providers/configs without modifying existing code |
| **L** — Liskov Substitution | `EmbeddingProvider` implementations | Any provider can be used interchangeably |
| **I** — Interface Segregation | `EmbeddingProvider` Protocol | Minimal contract — only one method |
| **D** — Dependency Inversion | `AgentService`, `EmbeddingProvider` | High-level modules depend on abstractions |

---

## Replaceability Matrix

| Component | Current | Replace With | Effort | Files to Touch |
|-----------|---------|-------------|--------|----------------|
| AI Framework | Agno | LangChain, CrewAI, Claude SDK | Low | `agent.py`, `agent_service.py` |
| LLM Model | Gemini 2.5 Flash | GPT-4, Claude, Mistral | Low | `agent.py` (1 line) |
| Embedding Provider | Gemini text-embedding-004 | OpenAI, local model | Low | Add class in `providers.py` (1 line to swap) |
| Vector DB | ChromaDB | Pinecone, Weaviate, Qdrant | Medium | `vector_db/setup.py` |
| Web Framework | FastAPI | Flask, Django | Low | `main.py` only |
| Knowledge Data | Python + Pydantic | Database, CMS, YAML | Medium | `knowledge/` files |

---

## Directory Structure

```
idoClaude/
├── ARCHITECTURE.md        # This file
├── CLAUDE.md              # Claude Code guidelines
├── Dockerfile
├── railway.json
│
├── frontend/              # Vue 3 + Vite
│   ├── src/
│   └── package.json
│
└── backend/               # FastAPI + Agno
    ├── main.py            # API layer — FastAPI routes
    ├── agent.py           # Agent layer — factory + tool registration
    ├── start.sh           # Dev startup script (activates venv)
    ├── requirements.txt
    │
    ├── services/          # Service layer
    │   └── agent_service.py   # AgentService class
    │
    ├── tools/             # Tool layer — pure Python
    │   ├── search_portfolio.py     # RAG search — main tool
    │   ├── get_contact_info.py     # exact contact + availability
    │   └── send_contact_email.py   # action — sends email via Resend
    │
    ├── knowledge/         # Data layer — Pydantic models
    │   ├── models.py          # Project, Skill, Experience
    │   ├── projects.py
    │   ├── skills.py
    │   └── experience.py
    │
    ├── vector_db/         # Vector search layer
    │   ├── providers.py       # EmbeddingProvider Protocol
    │   ├── setup.py           # ChromaDB client + search
    │   └── index_data.py      # Indexing script
    │
    └── storage/
        └── chroma/            # ChromaDB persistent storage
```

---

## Key Architectural Decisions

### ADR-1: AgentService wrapper over direct agno calls
**Problem:** `main.py` was calling `portfolio_agent.run()` directly — the API layer knew agno internals.
**Decision:** Introduce `AgentService` as a thin wrapper. API layer calls `.chat()` and gets a plain string back.
**Result:** Replacing agno touches only `agent_service.py`, never the API layer.

### ADR-2: @tool decorator applied at agent.py, not in tool files
**Problem:** All tool files imported agno and used `@tool`, making them untestable without the framework.
**Decision:** Tool files are pure Python. `agent.py` wraps them with `tool()` at registration time.
**Result:** Tools are independently testable; framework swap requires changing one file.

### ADR-3: create_agent() factory instead of global singleton
**Problem:** `portfolio_agent = Agent(...)` ran on import — untestable, no control over creation.
**Decision:** `create_agent()` factory function — agent is created only when called.
**Result:** No module-level side effects; multiple configurations possible (test vs production).

### ADR-4: EmbeddingProvider Protocol for vector search
**Problem:** `get_embedding()` hardcoded Gemini API calls — impossible to swap or mock.
**Decision:** `EmbeddingProvider` Protocol with `GeminiEmbeddingProvider` and `NullEmbeddingProvider`.
**Result:** Adding a new embedding provider = one new class, zero other changes.

### ADR-5: Pydantic models for knowledge data
**Problem:** Raw Python dicts had no validation, no types, no IDE support — typos failed silently at runtime.
**Decision:** `Project`, `Skill`, `Experience` Pydantic BaseModel classes.
**Result:** Validation at startup, full IDE autocomplete, attribute access instead of dict keys.

### ADR-7: All knowledge in a single ChromaDB collection
**Problem:** Only projects were indexed in ChromaDB. Skills and experience used hardcoded Python dict lookups — no semantic understanding.
**Decision:** Index all portfolio data (projects, skills, experience) into one `portfolio_knowledge` ChromaDB collection with a `type` metadata field for filtering.
**Result:** The agent can semantically find relevant knowledge across all data types with one tool call. "Leadership experience" finds the Bezeq role even without exact keyword match.

### ADR-8: Reduce agent toolset from 11 to 4
**Problem:** 11 tools created decision overhead — Gemini had to choose between `search_projects`, `search_projects_semantic`, `get_skill_level`, `list_skills_by_category`, `get_experience_details`, etc.
**Decision:** Replace all data-lookup tools with one `search_portfolio` RAG tool. Keep only action/exact-data tools: `send_contact_email`, `get_contact_information`, `get_hiring_availability`.
**Result:** Simpler agent reasoning, fewer wrong tool selections, all data queries go through RAG.

### ADR-9: AgentOS playground for debugging
**Problem:** No way to inspect tool calls, session history, or token usage without adding print statements.
**Decision:** Add `playground.py` using `agno.os.AgentOS` on port 7777. Connect to `https://os.agno.com` for a full debug UI.
**Result:** Every tool call, its inputs/outputs, timing, and session history is visible in the UI without touching production code.

### ADR-6: session_id as the conversation memory key
**Problem:** Without persistence, every `agent.run()` call started from scratch — the agent had no memory of previous messages in the same visit.
**Decision:** Use `SqliteDb` as the Agno storage backend with `add_history_to_context=True`. The `session_id` (generated once per tab visit and stored in the browser's `sessionStorage`) is passed with every request and used by Agno as the lookup key into SQLite.
**How it works:**
- First message: Agno saves the exchange (user + assistant) to `portfolio.db` under the `session_id`
- Every subsequent message: Agno queries `portfolio.db` for all previous runs with that `session_id` and prepends them to the prompt before calling Gemini
- `num_history_runs=10` caps how far back it looks, preventing unbounded prompt growth
- Tab close = new `session_id` on next visit = fresh conversation (intentional — no cross-visit persistence needed)
**Result:** The agent remembers everything said within a single visit without requiring any login or user identity.
