# RAG — How It Works in idoClaude

## What is RAG

RAG (Retrieval Augmented Generation) solves the problem of giving an LLM access to private data it wasn't trained on. Instead of stuffing all your data into every prompt, you store it externally and retrieve only the relevant pieces at query time.

---

## What's in RAG

All portfolio knowledge lives in a single ChromaDB collection (`portfolio_knowledge`) — 9 documents total:

| ID | Type | Content |
|---|---|---|
| `project-ido-claude` | `project` | idoPortfolio AI assistant |
| `project-shopping-cart` | `project` | E-Commerce app |
| `project-location-social-platform` | `project` | Android app |
| `skills-frontend` | `skill_group` | Vue.js, React, JS, TS... |
| `skills-backend` | `skill_group` | Node.js, Express, Firebase... |
| `skills-tools` | `skill_group` | Vite, Pinia, Docker... |
| `experience-trackboxai` | `experience` | Front-End Dev at Trackbox.ai |
| `experience-bezeq-international` | `experience` | Shift Supervisor at Bezeq |
| `experience-clal-insurance` | `experience` | Sales Rep at Clal Insurance |

---

## Step 1 — Indexing (Run After Any Data Change)

```bash
cd backend && python3 vector_db/index_data.py
```

This runs `index_projects()`, `index_skills()`, and `index_experience()` from `vector_db/setup.py`.

Each document gets converted to a 768-dimensional vector by Gemini's `text-embedding-004` model and stored in ChromaDB:

```
"Ido Cohen's Frontend Skills: Vue.js 90%, JS 95%..."
        │
        ▼
Gemini text-embedding-004
        │
        ▼
[0.023, -0.441, 0.887, ...]   ← 768 numbers representing meaning
        │
        ▼
ChromaDB  →  backend/storage/chroma/  (on disk)
```

---

## Step 2 — What Vectors Are

The embedding model converts text into 768 numbers that capture meaning. Similar meanings produce mathematically similar vectors:

```
"Vue skills"        →  [0.21, -0.09, 0.88, ...]
"frontend mastery"  →  [0.22, -0.08, 0.91, ...]  ← close = similar meaning
"cooking recipe"    →  [-0.8,  0.54, 0.02, ...]  ← far = different meaning
```

ChromaDB finds the closest vectors using cosine similarity — that's how "Vue expertise" finds the frontend skills document even though those words don't appear in it.

---

## Step 3 — Query Flow

**User asks:** `"What are Ido's Vue skills?"`

```
Browser → POST /api/chat → main.py → agent_service → agent.run()
                                                           │
                                               Agno sends to Gemini:
                                               message + tool schemas
                                                           │
                                                           ▼
                                               Gemini decides:
                                               "call search_portfolio(
                                                  query='Vue skills',
                                                  type_filter='skill_group'
                                                )"
```

---

## Step 4 — The Tool Runs (RAG Happens Here)

```python
# tools/search_portfolio.py
def search_portfolio(query, type_filter=None):
    results = _search(query, n_results=4, type_filter=type_filter)
    #         ↑ calls vector_db/setup.py → search_portfolio()

# vector_db/setup.py
def search_portfolio(query, n_results, type_filter):
    # 1. Convert query to vector
    query_embedding = get_embedding(query)          # → vector_db/providers.py
    # → [0.21, -0.09, 0.88, ...]

    # 2. Find closest documents in ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        where={"type": "skill_group"},              # optional filter
        n_results=4
    )
    # → frontend skills document (distance 0.05) ✅

    # 3. Return document content + metadata
    return [{ "content": "...", "type": "skill_group", "relevance": 0.95 }]
```

---

## Step 5 — Gemini Writes the Answer

Agno appends the tool result to the conversation and calls Gemini again:

```
[system]   you are Ido's assistant...
[user]     what are Ido's Vue skills?
[tool]     "Ido Cohen's Frontend Skills:
            - JavaScript: 95%
            - Vue.js: 90%
            - Vue 3 / Composition API: 90%..."
```

Gemini now has real data and writes a natural language response.

---

## Full Flow

```
USER: "Vue skills?"
         │
         ▼
      App.vue → ai.service.ts → POST /api/chat
                                      │
                                   main.py
                                      │
                               agent_service.py
                                      │
                               Agno → Gemini
                                      │
                           "call search_portfolio"
                                      │
                       ┌──────────────▼──────────────┐
                       │         RAG RUNS             │
                       │                              │
                       │  query → get_embedding()     │ ← providers.py (Gemini API)
                       │  vector → ChromaDB.query()   │ ← cosine similarity search
                       │  return document content     │
                       └──────────────┬──────────────┘
                                      │
                               Gemini: reads result → writes answer
                                      │
      USER sees response ◄────────────┘
```

---

## Key Files

| File | Role |
|---|---|
| `backend/vector_db/providers.py` | `EmbeddingProvider` protocol + `GeminiEmbeddingProvider` |
| `backend/vector_db/setup.py` | ChromaDB client, `index_*()` functions, `search_portfolio()` |
| `backend/vector_db/index_data.py` | Indexing script — run after any knowledge change |
| `backend/tools/search_portfolio.py` | Tool function — single RAG entry point for the agent |
| `backend/knowledge/` | Source of truth — edit here, then re-index |
| `backend/storage/chroma/` | ChromaDB data on disk |

---

## Viewing the Data

```bash
cd backend && source venv/bin/activate && python3 -c "
from vector_db.setup import get_portfolio_collection
col = get_portfolio_collection()
data = col.get()
for id, doc, meta in zip(data['ids'], data['documents'], data['metadatas']):
    print(f'[{meta[\"type\"]}] {id}')
    print(doc[:120])
    print()
"
```

---

## Interview Q&A

**What is RAG?**
Retrieval-Augmented Generation — retrieve relevant documents from a vector DB at query time, inject them into the LLM prompt. The LLM answers based on real data, not just training.

**Why not just put everything in the prompt?**
Context window limits. RAG retrieves only the relevant chunks, keeping the prompt small and focused.

**What's a vector embedding?**
Text converted to numbers representing meaning. Similar meanings → similar numbers. "Vue expertise" and "frontend skills" produce vectors that are mathematically close.

**What's cosine similarity?**
The angle between two vectors. Score near 1.0 = same meaning, near 0.0 = unrelated. ChromaDB returns this for every search result.

**What database did you use?**
ChromaDB — embedded vector database (runs inside the Python process, no separate server). Like SQLite but for vectors.

**How do you keep the data fresh?**
Edit `knowledge/*.py` → run `python3 vector_db/index_data.py` → ChromaDB updates.

**What's chunking?**
Splitting large documents into smaller pieces before indexing. Not needed here — documents are already small (150-400 tokens each).
