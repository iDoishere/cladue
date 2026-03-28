import chromadb
from chromadb.config import Settings
from pathlib import Path
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from vector_db.providers import get_default_provider, EmbeddingProvider

backend_dir = Path(__file__).parent.parent

env_file = backend_dir / ".env"
if env_file.exists():
    load_dotenv(env_file)

_chroma_client = None
_collection = None
_provider: EmbeddingProvider = get_default_provider()


def get_embedding(text: str) -> List[float]:
    return _provider.embed(text)


def get_portfolio_collection():
    """Single collection for all portfolio knowledge."""
    global _chroma_client, _collection

    if _collection is not None:
        return _collection

    chroma_path = backend_dir / "storage" / "chroma"
    _chroma_client = chromadb.PersistentClient(
        path=str(chroma_path),
        settings=Settings(anonymized_telemetry=False, allow_reset=True)
    )

    _collection = _chroma_client.get_or_create_collection(
        name="portfolio_knowledge",
        metadata={"description": "All of Ido Cohen's portfolio knowledge"}
    )

    return _collection


# Keep old name as alias for backward compatibility
def get_vector_db():
    return get_portfolio_collection()


def _clear_collection(collection):
    try:
        existing = collection.get()
        if existing and existing['ids']:
            collection.delete(ids=existing['ids'])
            print(f"🗑️  Cleared {len(existing['ids'])} existing documents")
    except Exception as e:
        print(f"Note: Could not clear existing data: {e}")


def index_projects(projects) -> int:
    collection = get_portfolio_collection()
    _clear_collection(collection)

    documents, embeddings, metadatas, ids = [], [], [], []

    for project in projects:
        text = f"""Project: {project.title}

Description: {project.description}

Technologies: {', '.join(project.technologies)}

Features:
{chr(10).join('- ' + f for f in project.features)}

Year: {project.year}
"""
        documents.append(text.strip())
        embeddings.append(get_embedding(text.strip()))
        ids.append(f"project-{project.id}")
        metadatas.append({
            "type": "project",
            "id": project.id,
            "title": project.title,
            "description": project.description,
            "technologies": ", ".join(project.technologies),
            "year": str(project.year),
        })

    collection.add(documents=documents, embeddings=embeddings, metadatas=metadatas, ids=ids)
    print(f"✅ Indexed {len(projects)} projects")
    return len(projects)


def index_skills(skills_data: Dict) -> int:
    collection = get_portfolio_collection()
    documents, embeddings, metadatas, ids = [], [], [], []

    for category, skills in skills_data.items():
        sorted_skills = sorted(skills, key=lambda s: s.level, reverse=True)
        skill_lines = "\n".join(f"- {s.name}: {s.level}% proficiency" for s in sorted_skills)

        text = f"""Ido Cohen's {category.capitalize()} Skills:

{skill_lines}

Category: {category}
Top skill: {sorted_skills[0].name} at {sorted_skills[0].level}%
All skills: {', '.join(s.name for s in sorted_skills)}
"""
        documents.append(text.strip())
        embeddings.append(get_embedding(text.strip()))
        ids.append(f"skills-{category}")
        metadatas.append({
            "type": "skill_group",
            "category": category,
            "title": f"{category.capitalize()} Skills",
            "top_skill": sorted_skills[0].name,
            "top_level": str(sorted_skills[0].level),
            "skill_names": ", ".join(s.name for s in sorted_skills),
        })

    collection.add(documents=documents, embeddings=embeddings, metadatas=metadatas, ids=ids)
    print(f"✅ Indexed {len(skills_data)} skill groups")
    return len(skills_data)


def index_experience(experience_data) -> int:
    collection = get_portfolio_collection()
    documents, embeddings, metadatas, ids = [], [], [], []

    for exp in experience_data:
        techs = ", ".join(exp.technologies) if exp.technologies else "N/A"
        resp_text = "\n".join(f"- {r}" for r in exp.responsibilities)
        current_tag = "Current role" if exp.current else "Previous role"

        text = f"""Work Experience: {exp.title} at {exp.company}
{current_tag} | Period: {exp.period} | Location: {exp.location}

Responsibilities:
{resp_text}

Technologies: {techs}
"""
        documents.append(text.strip())
        embeddings.append(get_embedding(text.strip()))
        ids.append(f"experience-{exp.company.lower().replace('.', '').replace(' ', '-')}")
        metadatas.append({
            "type": "experience",
            "company": exp.company,
            "title": exp.title,
            "period": exp.period,
            "current": str(exp.current),
            "technologies": techs,
        })

    collection.add(documents=documents, embeddings=embeddings, metadatas=metadatas, ids=ids)
    print(f"✅ Indexed {len(experience_data)} experience entries")
    return len(experience_data)


def search_portfolio(query: str, n_results: int = 4, type_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    """Semantic search across all portfolio knowledge."""
    collection = get_portfolio_collection()

    if collection.count() == 0:
        return []

    query_embedding = get_embedding(query)
    where = {"type": type_filter} if type_filter else None

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(n_results, collection.count()),
        where=where,
        include=["documents", "metadatas", "distances"]
    )

    matches = []
    if results and results['metadatas']:
        for i, metadata in enumerate(results['metadatas'][0]):
            distance = results['distances'][0][i] if results.get('distances') else None
            matches.append({
                **metadata,
                "content": results['documents'][0][i],
                "relevance": round(1 - distance, 3) if distance else None,
            })

    return matches


# Backward compat
def search_similar_projects(query: str, n_results: int = 3) -> List[Dict[str, Any]]:
    results = search_portfolio(query, n_results=n_results, type_filter="project")
    return [{
        "id": r.get("id", ""),
        "title": r.get("title", ""),
        "description": r.get("description", ""),
        "technologies": r.get("technologies", "").split(", "),
        "year": int(r.get("year", 0)),
        "similarity_score": r.get("relevance"),
    } for r in results]
