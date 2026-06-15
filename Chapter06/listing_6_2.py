from typing import Literal, TypedDict, Callable, Any


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
        context = {  #A
            "task": task,
            "previous_output": output,
            "critique": critique["feedback"],
        }
    return output
