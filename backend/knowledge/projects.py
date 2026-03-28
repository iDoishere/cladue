from knowledge.models import Project

projects_data = [
    Project(
        id="ido-claude",
        title="idoPortfolio - AI-Powered Conversational Portfolio",
        description="AI-powered portfolio assistant built with Vue 3 and FastAPI. Visitors chat with an intelligent agent that answers questions about Ido's projects, skills, and experience — and can even send him a message directly from the chat.",
        technologies=["Vue 3", "TypeScript", "FastAPI", "Python", "Agno", "Gemini", "ChromaDB", "RAG", "Node.js"],
        features=[
            "Conversational AI agent powered by Gemini 2.5 Flash",
            "RAG (Retrieval-Augmented Generation) with ChromaDB vector search",
            "Session memory — agent remembers context across the conversation",
            "Email tool — recruiters can contact Ido directly from the chat",
            "10 custom tools for projects, skills, experience, and contact",
            "AgentOS integration for real-time traces and debugging",
            "Animated Vue 3 frontend with markdown rendering"
        ],
        year=2025,
        github="https://github.com/iDoishere",
        demo=None
    ),
    Project(
        id="shopping-cart",
        title="Shopping Cart - Full-Stack E-Commerce Application",
        description="Full-stack e-commerce app with authentication, product catalog with search, sort, and filter, and real-time cart updates.",
        technologies=["React", "Redux", "MongoDB", "Node.js", "Express", "REST APIs"],
        features=[
            "User authentication and registration",
            "Product catalog with search, sort, and filter",
            "Real-time cart updates",
            "REST API backend with Express and Node.js",
            "MongoDB for persistent data storage",
            "Redux for global state management"
        ],
        year=2019,
        github="https://github.com/iDoishere",
        demo=None
    ),
    Project(
        id="location-social-platform",
        title="Location-Based Social Platform - Android Application",
        description="Native Android app enabling users to share and discover real-time updates from public locations with integrated mapping and proximity detection.",
        technologies=["Android Studio", "Java", "XML", "Firebase Realtime Database", "Google Maps API"],
        features=[
            "Real-time updates from public locations",
            "Google Maps integration with custom markers",
            "Proximity detection and location-based filtering",
            "Firebase Realtime Database for live data sync",
            "Google Authentication for secure sign-in",
            "Native Android UI with XML layouts"
        ],
        year=2020,
        github=None,
        demo=None
    ),
]
