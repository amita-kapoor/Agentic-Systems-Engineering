strategy = {  # Initial strategy and assumptions
    "prompt_template": "Fix failing tests",
    "assumptions": ["input data is clean"],
}

task = "Fix failing tests across repositories"

output = run_agent(task, strategy)  # Execute the task using the current strategy

signal = {  # Collect feedback across task executions
    "success_rate": metrics.success_rate(task_family=task),
    "common_failures": metrics.recurring_failures(task_family=task),
    "cost_per_task": metrics.avg_cost(task_family=task),
}

critique = critic(
    {  # Evaluate the effectiveness of the strategy
        "task": task,
        "strategy": strategy,
        "signal": signal,
    }
)

updated_strategy = strategy_updater(
    {  # Update the strategy based on accumulated feedback
        "previous_strategy": strategy,
        "critique": critique["feedback"],
    }
)

output = run_agent(task, updated_strategy)  # Execute the task using the revised strategy
