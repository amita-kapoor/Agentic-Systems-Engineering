def external_eval_reflect(task, generator_model, evaluator_model, max_iters=3):
    if max_iters < 1:
        raise ValueError("max_iters must be at least 1")  #A

    context = {"task": task}

    for _ in range(max_iters):
        output = generator_model(context)  #B
        critique = evaluator_model({  #C
            "task": task,
            "output": output,
            "instruction": "Evaluate the output against the task and return a structured critique",
        })

        if critique["status"] == "acceptable":
            return output

        context["previous_output"] = output
        context["critique"] = critique["feedback"]  #D #E

    return output
