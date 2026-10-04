task = "Fix failing test in order processing"

prompt = {  # Initial task prompt
    "task": task,
    "instruction": "Fix the failing test case",
}

output = generator(prompt)  # Generate a candidate solution

signal = run_tests(output)  # Obtain execution feedback from tests

critique = critic(
    {  # Evaluate the solution using the test signal
        "task": task,
        "output": output,
        "signal": signal,
    }
)

refined_prompt = {  # Incorporate critique into the next iteration
    "task": task,
    "previous_output": output,
    "critique": critique["feedback"],
}

refined_output = generator(refined_prompt)  # Generate an improved solution
