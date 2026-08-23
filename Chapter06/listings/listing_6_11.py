def external_eval_reflect(task, generator_model, evaluator_model, max_iters=3):
    if max_iters < 1:
        raise ValueError(
            "max_iters must be at least 1"
        )  # Reflection requires at least one iteration

    context = {"task": task}

    for _ in range(max_iters):
        output = generator_model(context)  # Generate candidate output using the primary model
        critique = evaluator_model(
            {  # Evaluate output using an independent model
                "task": task,
                "output": output,
                "instruction": (
                    "Evaluate the output against the task and return a structured critique"
                ),
            }
        )

        if critique["status"] == "acceptable":
            return output

        context["previous_output"] = output
        context["critique"] = critique[
            "feedback"
            # Critique must follow a structured schema with "status" and "feedback", enforce this
            # through prompt design or output parsing; Update context with evaluator feedback for
            # the next iteration
        ]

    return output
