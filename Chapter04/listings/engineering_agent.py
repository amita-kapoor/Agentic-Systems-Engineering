class EngineeringAgent:
    def __init__(self, llm, semantic_memory, episodic_memory=None):
        self.llm = llm
        self.semantic = semantic_memory
        self.episodic = episodic_memory  # can be None

    def diagnose(self, logs):
        context = []

        # Semantic memory (always present)
        context.append(f"Service timeout: {self.semantic['timeout']}ms")

        # Episodic memory (optional)
        if self.episodic:
            episode = self.episodic.get("503 error")
            if episode:
                context.append(f"Prior incident summary: {episode}")

        prompt = f"""
Diagnose the cause of intermittent 503 errors.
Logs:
{logs}
Context:
{chr(10).join(context)}
Explain your reasoning and propose the next step.
"""
        return self.llm(prompt)
