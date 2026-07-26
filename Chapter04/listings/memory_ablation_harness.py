def memory_ablation_test(agent, logs):
    with_memory = agent.diagnose(logs)

    # Restore the agent afterwards, so the test can be run more than once and
    # the caller is not handed back an agent that has lost its episodic memory.
    saved_episodic = agent.episodic
    agent.episodic = None
    try:
        without_memory = agent.diagnose(logs)
    finally:
        agent.episodic = saved_episodic

    return {"with_memory": with_memory, "without_memory": without_memory}
