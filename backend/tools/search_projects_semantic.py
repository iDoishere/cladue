from agno.tools import tool
from vector_db.setup import search_similar_projects
from knowledge.projects import projects_data
import json


@tool
def search_projects_semantic(query: str, max_results: int = 2) -> str:
    """
    Search projects using semantic/meaning-based search (NOT keyword matching).
    Use this when users ask about projects in natural language.

    Examples of when to use:
    - "projects with real-time features"
    - "apps that use databases"
    - "work involving location or maps"
    - "chat or messaging systems"

    Args:
        query: Natural language description of what to search for
        max_results: Maximum number of projects to return (default: 2)

    Returns:
        JSON string with semantically matching projects
    """
    try:
        # Use vector search for semantic matching
        matches = search_similar_projects(query, n_results=max_results)

        # If vector search returns results, use them
        if matches:
            # Enrich results with full project data
            enriched_matches = []
            for match in matches:
                # Find full project data
                full_project = next(
                    (p for p in projects_data if p['id'] == match['id']),
                    None
                )
                if full_project:
                    enriched_matches.append({
                        **full_project,
                        "similarity_score": match.get('similarity_score')
                    })

            return json.dumps({
                "search_type": "semantic",
                "query": query,
                "found": len(enriched_matches),
                "projects": enriched_matches
            }, indent=2)

        # Fallback: if no vector results, return empty
        return json.dumps({
            "search_type": "semantic",
            "query": query,
            "found": 0,
            "projects": [],
            "note": "No semantically similar projects found"
        }, indent=2)

    except Exception as e:
        # If vector search fails, return error info
        return json.dumps({
            "search_type": "semantic",
            "query": query,
            "error": str(e),
            "note": "Vector search encountered an error. The database may need to be indexed first."
        }, indent=2)
