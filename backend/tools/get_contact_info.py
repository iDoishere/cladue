from agno.tools import tool

@tool
def get_contact_information() -> str:
    """
    Get Ido's contact information and professional links.

    Returns:
        Contact details, email, portfolio link, and preferred contact method
    """
    return """**Contact Information:**

📧 **Email:** idoisher2@gmail.com
🌐 **Portfolio:** https://portfoliolo.firebaseapp.com/
📍 **Location:** Rosh Ashlain, Israel

**Best Way to Reach Out:**
Send an email to idoisher2@gmail.com with:
• Position/project details
• Tech stack requirements
• Team information

Ido typically responds within 24-48 hours and is open to discussing:
✓ Full-stack development opportunities
✓ Vue.js/React projects
✓ Remote or hybrid positions in Israel
✓ Contract/consulting work
"""


@tool
def get_hiring_availability() -> str:
    """
    Check if Ido is open to new opportunities and what he's looking for.

    Returns:
        Information about job preferences and availability
    """
    return """**Current Status & Opportunities:**

🟢 **Open to Opportunities**
Currently employed at Tigloo but open to the right opportunity.

**What Ido is Looking For:**
✓ Full-stack or frontend-focused roles
✓ Modern tech stack (Vue.js, React, Node.js)
✓ Collaborative, growth-oriented teams
✓ Challenging projects that push technical boundaries
✓ Remote-friendly or hybrid positions in Israel

**Ideal Role:**
Senior Frontend Developer or Full-Stack Developer position where he can:
• Lead Vue.js/React architecture decisions
• Mentor junior developers
• Work on complex, user-facing applications
• Continue growing backend expertise

**Not Interested In:**
✗ Pure backend-only roles
✗ Legacy tech stacks (no Vue 2, old PHP, jQuery-heavy)
✗ Positions requiring relocation outside Israel

**Best Fit:**
Companies building modern web applications with a focus on user experience and code quality.
"""


@tool
def suggest_next_steps(user_goal: str) -> str:
    """
    Suggest what the user should do next based on their goal.

    Args:
        user_goal: What the user wants (e.g., "hire Ido", "learn more", "see portfolio")

    Returns:
        Actionable next steps tailored to user's goal
    """
    suggestions = {
        "hire": """**Next Steps to Hire Ido:**

1. **Review Portfolio:** Check out https://portfoliolo.firebaseapp.com/ for live projects
2. **Prepare Details:** Think about role requirements, tech stack, team structure
3. **Reach Out:** Email idoisher2@gmail.com with:
   • Position overview
   • Tech stack & tools
   • Team size & structure
   • Salary range (if applicable)
4. **Schedule Chat:** Propose a time for a 30-min intro call

**Pro Tip:** Mention specific Vue.js or React challenges your team is facing - Ido loves solving complex UI problems!
""",

        "learn": """**To Learn More About Ido:**

1. Ask me specific questions about:
   • "What projects has Ido built with Firebase?"
   • "What's Ido's Vue.js skill level?"
   • "Tell me about Ido's current role"

2. Explore his portfolio: https://portfoliolo.firebaseapp.com/

3. See his GitHub for code samples (if available)

**What would you like to know more about?** Projects, skills, or experience?
""",

        "portfolio": """**Explore Ido's Portfolio:**

🌐 **Live Portfolio:** https://portfoliolo.firebaseapp.com/

**Featured Projects:**
1. **Android App** - Real-time location tracking with Firebase
2. **Chat Application** - Full-stack real-time messaging

**Or ask me:**
• "Show me projects using React"
• "What's the most complex project Ido built?"
• "Tell me about the Android app features"
""",
    }

    # Match user goal to suggestion
    goal_lower = user_goal.lower()
    if "hire" in goal_lower or "job" in goal_lower or "position" in goal_lower:
        return suggestions["hire"]
    elif "portfolio" in goal_lower or "work" in goal_lower or "examples" in goal_lower:
        return suggestions["portfolio"]
    else:
        return suggestions["learn"]
