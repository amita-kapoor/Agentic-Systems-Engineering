def rule_based_reflect(task, model, rules, max_iters=3):
    if max_iters < 1:
        raise ValueError("max_iters must be at least 1")  #A

    context = {
        "task": task,
        "rules": rules,
    }

    for _ in range(max_iters):
        output = model({  #B
            "role": "generator",
            "context": context,
        })

        critique = model({  #C
            "role": "critic",
            "task": task,
            "output": output,
            "rules": rules,
            "instruction": "Identify violations of the given rules",
        })

        if critique["status"] == "acceptable":
            return output

        context["previous_output"] = output
        context["critique"] = critique["feedback"]  #D #E

    return output
