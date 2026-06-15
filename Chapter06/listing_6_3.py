from typing import Literal, TypedDict, Callable, Any


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
            return output, plan  #A
        plan = planner({  #B
            "task": task,
            "previous_plan": plan,
            "execution_feedback": critique["feedback"],
        })
    return output, plan  #C
