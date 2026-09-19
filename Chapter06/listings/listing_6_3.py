from typing import Any, Callable, Literal, TypedDict


class Critique(TypedDict):
    status: Literal["acceptable", "needs_revision"]
    issues: list[str]
    feedback: str


def double_loop_reflect(
    task: Any,
    planner: Callable[[Any], Any],
    executor: Callable[[Any], Any],
    critic: Callable[[Any, Any], Critique],
    max_iters: int = 3,
) -> tuple[Any, Any]:
    """
    Executes a double-loop reflection pattern.

    Returns:
        A tuple containing the final (Output, Plan).
    """
    plan = planner(task)
    for _ in range(max_iters):
        output = executor(plan)
        critique = critic(task, output)
        if critique["status"] == "acceptable":
            return output, plan  # Return both so the successful plan is available for inspection
        plan = planner(
            {  # Critique now updates the plan, not just the output
                "task": task,
                "previous_plan": plan,
                "execution_feedback": critique["feedback"],
            }
        )
    return (
        output,
        plan,
        # If max_iters is exhausted without an "acceptable" status, returning the last output AND
        # the revised plan is crucial. In double-loop learning, inspecting this final adapted plan
        # provides deep insight into where the agent got stuck
    )
