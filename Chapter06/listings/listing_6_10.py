def rule_based_reflect(task, model, rules, max_iters=3):
    if max_iters < 1:
        raise ValueError(
            "max_iters must be at least 1"
        )  # Reflection requires at least one iteration

    context = {
        "task": task,
        "rules": rules,
    }

    for _ in range(max_iters):
        output = model(
            {  # Generate candidate output
                "role": "generator",
                "context": context,
            }
        )

        critique = model(
            {  # Evaluate output against explicit rules
                "role": "critic",
                "task": task,
                "output": output,
                "rules": rules,
                "instruction": "Identify violations of the given rules",
            }
        )

        if critique["status"] == "acceptable":
            return output

        context["previous_output"] = output
        context["critique"] = critique[
            "feedback"
            # Critique must follow a structured schema with "status" and "feedback" enforce this
            # through prompt design or output parsing; Update context with rule-based critique for
            # next iteration
        ]

    return output
