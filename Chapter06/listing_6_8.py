def memory_augmented_reflect(task, model, memory, critic, max_iters=3):
    if max_iters < 1:
        raise ValueError("max_iters must be at least 1")  #A

    past_experiences = memory.retrieve(task)  #B
    context = {
        "task": task,
        "memory": past_experiences,
    }

    for _ in range(max_iters):
        output = model({  #C
            "role": "generator",
            "context": context,
        })

        signal = evaluate(output)  #D
        critique = critic({
            "task": task,
            "output": output,
            "signal": signal,
        })

        if critique["status"] == "acceptable":
            memory.store({  #E
                "task": task,
                "solution": output,
                "insight": "successful approach",
            })
            return output

        context["previous_output"] = output
        context["critique"] = critique["feedback"]  #F

        memory.store({  #G
            "task": task,
            "failure": output,
            "critique": critique["feedback"],
        })

    return output
