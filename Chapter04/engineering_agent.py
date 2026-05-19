class EngineeringAgent:
    def __init__(self, llm, semantic_memory, episodic_memory=None):
        self.llm = llm
        self.semantic = semantic_memory
        self.episodic = episodic_memory  # A

    def diagnose(self, logs):
        context = []

        # B
        context.append(f"Service timeout: {self.semantic['timeout']}ms")

        # C
        if self.episodic:
            episode = self.episodic.retrieve("503 error")
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


# A can be None
# B Semantic memory (always present)
# C Episodic memory (optional)
