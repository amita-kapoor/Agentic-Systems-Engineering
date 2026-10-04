task = "Fix failing tests in order processing"

plan = planner(
    {  # Generate an initial plan
        "task": task,
        "instruction": "Generate steps to fix failing tests",
    }
)

output = executor(plan)  # Execute the plan

signal = {  # Collect execution feedback
    "trace": collect_execution_trace(plan, output),
    "tool_calls": output.tool_calls,
    "errors": output.errors,
}

critique = critic(
    {  # Evaluate the effectiveness of the plan
        "task": task,
        "plan": plan,
        "output": output,
        "signal": signal,
    }
)

revised_plan = planner(
    {  # Revise the plan using critique feedback
        "task": task,
        "previous_plan": plan,
        "execution_feedback": critique["feedback"],
    }
)

output = executor(revised_plan)  # Execute the improved plan
