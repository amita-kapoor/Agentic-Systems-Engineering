strategy = {  #A
    "prompt_template": "Fix failing tests",
    "assumptions": ["input data is clean"],
}

task = "Fix failing tests across repositories"

output = run_agent(task, strategy)  #B

signal = {  #C
    "success_rate": metrics.success_rate(task_family=task),
    "common_failures": metrics.recurring_failures(task_family=task),
    "cost_per_task": metrics.avg_cost(task_family=task),
}

critique = critic({  #D
    "task": task,
    "strategy": strategy,
    "signal": signal,
})

updated_strategy = strategy_updater({  #E
    "previous_strategy": strategy,
    "critique": critique["feedback"],
})

output = run_agent(task, updated_strategy)  #F
