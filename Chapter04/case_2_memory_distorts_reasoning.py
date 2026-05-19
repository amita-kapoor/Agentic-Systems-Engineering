episodic_memory = {
    "503 error": "Previous incidents were caused by a database outage."
}

agent = EngineeringAgent(llm, semantic_memory, episodic_memory)
print(agent.diagnose(logs))
