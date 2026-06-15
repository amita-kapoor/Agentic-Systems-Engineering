task = "Fix failing tests in order processing"

plan = planner({  #A
    "task": task,
    "instruction": "Generate steps to fix failing tests",
})

output = executor(plan)  #B

signal = {  #C
    "trace": collect_execution_trace(plan, output),
    "tool_calls": output.tool_calls,
    "errors": output.errors,
}

critique = critic({  #D
    "task": task,
    "plan": plan,
    "output": output,
    "signal": signal,
})

revised_plan = planner({  #E
    "task": task,
    "previous_plan": plan,
    "execution_feedback": critique["feedback"],
})

output = executor(revised_plan)  #F
