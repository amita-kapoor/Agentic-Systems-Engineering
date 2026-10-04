def tool_grounded_reflect(task, generator, critic, tools, max_iters=3):
    if max_iters < 1:
        raise ValueError(
            "max_iters must be at least 1"
        )  # Reflection requires at least one iteration

    context = {"task": task}

    for _ in range(max_iters):
        output = generator(context)  # Generate candidate solution
        signal = tools.run(
            {
                "task": task,
                "output": output,
            }
            # Invoke external tools to verify output. Obtain external verification signals (tests,
            # APIs, validators)
        )
        critique = critic(
            {
                "task": task,
                "output": output,
                "signal": signal,
            }
        )  # Evaluate output using tool-generated evidence

        if critique["status"] == "acceptable":
            return output

        context["previous_output"] = output
        context["critique"] = critique[
            "feedback"
        ]  # Update context with critique for next iteration

    return output
