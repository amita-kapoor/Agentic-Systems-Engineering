from typing import Any, Callable, Literal, TypedDict


class Critique(TypedDict):
    status: Literal["acceptable", "needs_revision"]
    issues: list[str]
    feedback: str


def single_loop_reflect(
    task: str,
    generator: Callable[[Any], str],
    critic: Callable[[str, str], dict],
    max_iters: int = 3,
) -> str:
    context = task
    for _ in range(max_iters):
        output = generator(context)
        critique = critic(task, output)
        if critique["status"] == "acceptable":
            return output
        context = {  # Only the output is revised, approach and plan unchanged
            "task": task,
            "previous_output": output,
            "critique": critique["feedback"],
        }
    return output
