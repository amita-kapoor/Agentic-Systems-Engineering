def production_reflect(task, generator, planner, tools, critic, memory, rules=None, max_iters=3):
    if max_iters < 1:
        raise ValueError("max_iters must be at least 1")  #A

    # Retrieve past experience
    context = {
        "task": task,
        "memory": memory.retrieve(task),
        "rules": rules,
    }

    # Initial plan
    plan = planner(context)  #B

    for _ in range(max_iters):
        # Execute plan
        output = generator({
            "plan": plan,
            "context": context,
        })  #C

        # Observation layer
        signal = tools.run({
            "task": task,
            "output": output,
        })  #D

        # Evaluation layer (can combine multiple strategies)
        critique = critic({
            "task": task,
            "plan": plan,
            "output": output,
            "signal": signal,
            "rules": context.get("rules", None),
        })  #E

        if critique["status"] == "acceptable":
            memory.store({
                "task": task,
                "solution": output,
                "plan": plan,
            })  #F
            return output

        # Apply feedback (double-loop capable)
        plan = planner({
            "task": task,
            "previous_plan": plan,
            "feedback": critique["feedback"],
        })  #G

        context["previous_output"] = output
        context["critique"] = critique["feedback"]

        # Store failure for future learning
        memory.store({
            "task": task,
            "failure": output,
            "critique": critique["feedback"],
        })  #H

    return output
