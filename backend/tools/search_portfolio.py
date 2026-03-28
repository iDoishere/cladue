import json
from vector_db.setup import search_portfolio as _search


def search_portfolio(query: str, type_filter: str = None) -> str:
    """
    Semantic search across ALL of Ido's portfolio knowledge — projects, skills, experience.

    Use this for any question about Ido. It finds the most relevant knowledge chunks
    based on meaning, not keywords.

    Args:
        query: Natural language question (e.g. "Vue.js experience", "real-time projects", "leadership skills")
        type_filter: Optional filter — "project", "skill_group", or "experience"

    Returns:
        Relevant knowledge as formatted text
    """
    results = _search(query, n_results=4, type_filter=type_filter)

    if not results:
        return "No relevant information found."

    output = []
    for r in results:
        output.append(r.get("content", ""))

    return "\n\n---\n\n".join(output)
