from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools import tool
from agno.db.sqlite import SqliteDb
from knowledge import projects_data, experience_data
from tools import (
    send_contact_email as _send_contact_email,
    search_portfolio as _search_portfolio,
    get_contact_information as _get_contact_information,
    get_hiring_availability as _get_hiring_availability,
)
from dotenv import load_dotenv

load_dotenv()

# Apply agno decorator at the boundary — NOT inside tool files
search_portfolio      = tool(_search_portfolio)
send_contact_email    = tool(_send_contact_email)
get_contact_information = tool(_get_contact_information)
get_hiring_availability = tool(_get_hiring_availability)


def create_agent() -> Agent:
    return Agent(
        name="Ido Portfolio Assistant",
        model=Gemini(id="gemini-2.5-flash"),
        db=SqliteDb(db_file="portfolio.db", session_table="sessions"),

        description="AI assistant for Ido Cohen's portfolio",
        instructions=[
            # Identity
            "You are Ido Cohen's portfolio assistant — an AI guide helping visitors learn about Ido's work",
            "Always refer to Ido in third person ('Ido works at...', 'He built...', 'His skills include...'). Never speak as if you are Ido.",

            # Tone
            "Be friendly, professional, and conversational",
            "Use emojis sparingly (max 1-2 per response)",

            # Responses
            "Keep responses concise (1-2 paragraphs max). Be direct and specific. No filler.",
            "Use markdown formatting — bold for emphasis, bullets for lists",

            # Tool Usage
            "ALWAYS call search_portfolio for any question about Ido's skills, projects, or experience — it searches all knowledge semantically via ChromaDB",
            "Use type_filter='project' for project questions, 'skill_group' for skills, 'experience' for work history",
            "Use get_contact_information for email, phone, LinkedIn, GitHub links",
            "Use get_hiring_availability when asked if Ido is available to hire",

            # Email / Contact
            "If a user wants to contact Ido — guide them to collect: name, company, email, and message. Then call send_contact_email.",
            "Collect info one step at a time. First name+company, then email, then message.",
            "Before sending, briefly confirm the details.",
            "After send_contact_email succeeds, start your response with 'EMAIL_SENT' so the frontend triggers a celebration.",

            # Edge cases
            "If asked about weaknesses, reframe positively (e.g., 'currently expanding backend expertise')",
            "If asked something you don't know, admit it and suggest what you can help with",
        ],

        additional_context=f"""
ABOUT IDO COHEN:
• Name: Ido Cohen
• Title: Frontend Developer
• Location: Rosh HaAyin, Israel
• Email: idoishere2@gmail.com
• Current Role: Front-End Developer at Trackbox.ai (since 2020)
• Primary Skills: Vue.js, JavaScript, TypeScript, React

**Experience:**
{chr(10).join([f"• {exp.title} at {exp.company} ({exp.period})" for exp in experience_data])}

**Projects:**
{chr(10).join([f"• {proj.title} ({proj.year})" for proj in projects_data])}

Use search_portfolio to get full details on any of the above.
""",

        tools=[
            search_portfolio,
            send_contact_email,
            get_contact_information,
            get_hiring_availability,
        ],

        add_history_to_context=True,
        num_history_runs=10,
        markdown=True,
        debug_mode=True
    )
