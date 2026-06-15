def self_refine(task, model, max_iters=3):
    context = {"task": task}

    for _ in range(max_iters):
        draft = model({  #A
            "role": "generator",
            "task": context["task"],
            "instruction": "Produce a solution to the task",
        })

        critique = model({  #B
            "role": "critic",
            "task": context["task"],
            "output": draft,
            "instruction": "Identify errors, gaps, or inconsistencies",
        })

        refined = model({  #C
            "role": "refiner",
            "task": context["task"],
            "previous_output": draft,
            "critique": critique,
        })

        if critique["status"] == "acceptable":  #D
            return refined

        context["previous_output"] = refined

    return refined
