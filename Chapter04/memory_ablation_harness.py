def memory_ablation_test(agent, logs):
    with_memory = agent.diagnose(logs)

    agent.episodic = None

    without_memory = agent.diagnose(logs)

    return {
        "with_memory": with_memory,
        "without_memory": without_memory
    }
