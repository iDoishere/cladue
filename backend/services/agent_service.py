class AgentService:
    def __init__(self, agent):
        self._agent = agent

    def chat(self, message: str, session_id: str) -> str:
        response = self._agent.run(message, session_id=session_id)
        content = response.content or ""

        error_signals = ["429", "quota", "exhausted", "rate_limit", "resource_exhausted", '"error"', "RESOURCE_EXHAUSTED"]
        if any(s.lower() in content.lower() for s in error_signals):
            if any(s in content for s in ["429", "quota", "exhausted", "RESOURCE_EXHAUSTED"]):
                return "I'm getting too many requests right now. Please try again in a moment."
            return "Something went wrong on my end. Please try again."

        return content
