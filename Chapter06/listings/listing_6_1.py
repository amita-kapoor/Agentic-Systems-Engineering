from typing import Any, Callable, Literal, TypedDict


class Critique(TypedDict):  # Define the exact structure of  critique dictionary
    status: Literal["acceptable", "needs_revision"]
    issues: list[str]
    feedback: str


example_critique: Critique = {  # Example of a  structured critique output
    "status": "acceptable",
    "issues": ["missing validation", "incorrect assumption"],
    "feedback": "Explain what needs to change",
}


def reflect_and_improve(
    task: Any,
    generator: Callable[[Any], Any],
    critic: Callable[[Any, Any], Critique],
    max_iters: int = 3,
) -> Any:
    context: Any = task
    for _ in range(max_iters):
        output = generator(context)
        critique = critic(task, output)
        if critique["status"] == "acceptable":
            return output
        context = {
            "task": task,
            "previous_output": output,
            "critique": critique["feedback"],
        }
    return output
