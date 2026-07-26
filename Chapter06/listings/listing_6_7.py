def self_refine(task, model, max_iters=3):
    context = {"task": task}

    for _ in range(max_iters):
        draft = model(
            {  # Step 1: Generate
                "role": "generator",
                "task": context["task"],
                "instruction": "Produce a solution to the task",
            }
        )

        critique = model(
            {  # Step 2: Critique
                "role": "critic",
                "task": context["task"],
                "output": draft,
                "instruction": "Identify errors, gaps, or inconsistencies",
            }
        )

        refined = model(
            # Step 3: Refine. Note: In the first iteration, 'draft' acts as the initial
            # previous_output
            {
                "role": "refiner",
                "task": context["task"],
                "previous_output": draft,
                "critique": critique,
            }
        )

        if critique["status"] == "acceptable":  # Stopping condition (simplified)
            return refined

        context["previous_output"] = refined

    return refined
