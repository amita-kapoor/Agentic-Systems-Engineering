task = "Fix failing test in order processing"

prompt = {  #A
    "task": task,
    "instruction": "Fix the failing test case",
}

output = generator(prompt)  #B

signal = run_tests(output)  #C

critique = critic({  #D
    "task": task,
    "output": output,
    "signal": signal,
})

refined_prompt = {  #E
    "task": task,
    "previous_output": output,
    "critique": critique["feedback"],
}

refined_output = generator(refined_prompt)  #F
