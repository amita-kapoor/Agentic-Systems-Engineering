def tool_grounded_reflect(task, generator, critic, tools, max_iters=3):
    if max_iters < 1:
        raise ValueError("max_iters must be at least 1")  #A

    context = {"task": task}

    for _ in range(max_iters):
        output = generator(context)  #B
        signal = tools.run({
            "task": task,
            "output": output,
        })  #C
        critique = critic({
            "task": task,
            "output": output,
            "signal": signal,
        })  #D

        if critique["status"] == "acceptable":
            return output

        context["previous_output"] = output
        context["critique"] = critique["feedback"]  #E

    return output
