"""
Agno Playground — run this to test the agent with full logging/traces.

Usage:
    cd backend
    source venv/bin/activate
    python playground.py

Then open: https://os.agno.com
Add endpoint: http://localhost:7777
"""

from dotenv import load_dotenv
load_dotenv()

from agent import create_agent
from agno.os import AgentOS

agent = create_agent()

agent_os = AgentOS(
    id="ido-portfolio-os",
    agents=[agent],
    tracing=True,
)

app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app="playground:app", reload=False)
