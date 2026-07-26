def memory_augmented_reflect(task, model, memory, critic, max_iters=3):
    if max_iters < 1:
        raise ValueError(
            "max_iters must be at least 1"
        )  # Reflection requires at least one iteration; fail fast rather than return silently

    past_experiences = memory.retrieve(task)  # Retrieve relevant past experiences
    context = {
        "task": task,
        "memory": past_experiences,
    }

    for _ in range(max_iters):
        output = model(
            {  # Generate with memory context
                "role": "generator",
                "context": context,
            }
        )

        signal = evaluate(
            output
        )  # Evaluate the output using observable signals such as tests, logs, or traces
        critique = critic(
            {
                "task": task,
                "output": output,
                "signal": signal,
            }
        )

        if critique["status"] == "acceptable":
            memory.store(
                {  # Store successful pattern
                    "task": task,
                    "solution": output,
                    "insight": "successful approach",
                }
            )
            return output

        context["previous_output"] = output
        context["critique"] = critique["feedback"]  # Update context with critique

        memory.store(
            # Max iterations reached without acceptable output. Store failure pattern for future
            # learning
            {
                "task": task,
                "failure": output,
                "critique": critique["feedback"],
            }
        )

    return output
