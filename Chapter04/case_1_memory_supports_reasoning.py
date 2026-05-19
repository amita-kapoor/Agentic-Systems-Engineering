episodic_memory = {
    "503 error": "Previous incidents involved timeout mismatches under load."
}

semantic_memory = {
    "timeout": 2000
}

agent = EngineeringAgent(llm, semantic_memory, episodic_memory)
print(agent.diagnose(logs))
