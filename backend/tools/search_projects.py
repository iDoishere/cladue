from agno.tools import tool
from knowledge.projects import projects_data
import json


@tool
def search_projects(technology: str = None, keyword: str = None) -> str:
    """
    Search through Ido's projects by technology or keyword.
    Returns RAW project data - the AI will format it conversationally.

    Args:
        technology: Technology name (e.g., "Vue", "React", "Firebase", "Java")
        keyword: Keyword to search in project descriptions (e.g., "real-time", "chat", "maps")

    Returns:
        JSON string with matching projects (AI will format for user)
    """
    if not technology and not keyword:
        # Return all projects if no search criteria
        matches = projects_data
    else:
        matches = []
        for project in projects_data:
            # Check technology match
            if technology:
                tech_match = any(
                    technology.lower() in t.lower()
                    for t in project['technologies']
                )
                if tech_match:
                    matches.append(project)
                    continue

            # Check keyword match in description, title, or features
            if keyword:
                keyword_lower = keyword.lower()
                keyword_in_desc = keyword_lower in project['description'].lower()
                keyword_in_title = keyword_lower in project['title'].lower()
                keyword_in_features = any(
                    keyword_lower in feature.lower()
                    for feature in project['features']
                )

                if keyword_in_desc or keyword_in_title or keyword_in_features:
                    matches.append(project)

    # Return raw data as JSON - let AI format conversationally
    return json.dumps({
        "search_criteria": {
            "technology": technology,
            "keyword": keyword
        },
        "found": len(matches),
        "projects": matches
    }, indent=2)
