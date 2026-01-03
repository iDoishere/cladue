from agno.tools import tool
from knowledge import experience_data

@tool
def get_experience_details(company: str = None) -> str:
    """
    Get detailed information about Ido's work experience.

    Args:
        company: Optional company name to filter by (e.g., "Tigloo", "Bezek")

    Returns:
        Formatted work experience details with responsibilities
    """
    if company:
        # Search for specific company
        company_lower = company.lower()
        for exp in experience_data:
            if company_lower in exp['company'].lower():
                result = f"""**{exp['title']} at {exp['company']}**
Period: {exp['period']}
Location: {exp['location']}

**Key Responsibilities:**
{chr(10).join(f"• {resp}" for resp in exp['responsibilities'])}
"""
                return result
        return f"No experience found at {company}. Available companies: Tigloo, Bezek International, Clal Insurance"

    # Return all experience
    result = []
    for exp in experience_data:
        result.append(f"""**{exp['title']} at {exp['company']}** ({exp['period']})
{chr(10).join(f"• {resp}" for resp in exp['responsibilities'][:2])}
""")

    return "\n".join(result)


@tool
def get_current_role() -> str:
    """
    Get information about Ido's current position and what he does day-to-day.

    Returns:
        Details about current role at Tigloo
    """
    current = experience_data[0]  # First item is most recent

    return f"""**Current Position:**
{current['title']} at {current['company']} (since 2020)

**Day-to-Day Work:**
{chr(10).join(f"• {resp}" for resp in current['responsibilities'])}

**Key Focus:**
Building complex, reusable Vue.js components and modern web applications for enterprise clients.
"""
