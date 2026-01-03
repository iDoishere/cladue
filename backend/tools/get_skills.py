from agno.tools import tool
from knowledge.skills import all_skills, skills_data


@tool
def get_skill_level(skill_name: str) -> str:
    """
    Get Ido's proficiency level for a specific skill.

    Args:
        skill_name: Name of the skill (e.g., "Vue.js", "React", "JavaScript", "Node.js")

    Returns:
        Formatted string with skill level and category
    """
    # Search for the skill (case-insensitive)
    skill_lower = skill_name.lower()
    found_skill = None

    for skill in all_skills:
        if skill_lower in skill['name'].lower() or skill['name'].lower() in skill_lower:
            found_skill = skill
            break

    if not found_skill:
        # List all available skills as suggestion
        all_skill_names = [s['name'] for s in all_skills]
        return f"Skill '{skill_name}' not found. Available skills: {', '.join(all_skill_names)}"

    # Format the response
    level = found_skill['level']
    category = found_skill['category'].capitalize()

    # Determine proficiency description
    if level >= 90:
        proficiency = "Expert"
    elif level >= 80:
        proficiency = "Advanced"
    elif level >= 70:
        proficiency = "Proficient"
    else:
        proficiency = "Intermediate"

    return f"**{found_skill['name']}**\nProficiency: {level}% ({proficiency})\nCategory: {category}"


@tool
def list_skills_by_category(category: str = None) -> str:
    """
    List all skills, optionally filtered by category.

    Args:
        category: Category to filter by ("frontend", "backend", or "tools"). Leave empty for all skills.

    Returns:
        Formatted list of skills with their proficiency levels
    """
    if category:
        category_lower = category.lower()
        if category_lower not in skills_data:
            return f"Category '{category}' not found. Available categories: frontend, backend, tools"

        skills_list = skills_data[category_lower]
        title = f"{category.capitalize()} Skills"
    else:
        skills_list = all_skills
        title = "All Skills"

    # Sort by level descending
    sorted_skills = sorted(skills_list, key=lambda x: x['level'], reverse=True)

    # Format output
    result = [f"**{title}**\n"]
    for skill in sorted_skills:
        bar_length = skill['level'] // 5  # 20 chars max
        bar = "█" * bar_length + "░" * (20 - bar_length)
        result.append(f"{skill['name']:<20} {bar} {skill['level']}%")

    return "\n".join(result)
