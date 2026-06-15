@dataclass
class Plan:  #A
    focus_clauses: list[str]
    evidence_emphasis: list[str]
    notes: str = ""


PLANNER_SYSTEM = """You are a compliance planning assistant.
Given a product description and regulatory clauses, produce a JSON plan:
{
  "focus_clauses": [clause_id, ...],
  "evidence_emphasis": [string, ...],
  "notes": string
}
If a previous plan and execution feedback are provided, REVISE the plan to address the
feedback.
"""  #B


def planner(task: dict) -> Plan:
    parts = [  #C
        f"PRODUCT DESCRIPTION:\n{task['product_description']}",
        f"\nREGULATORY CLAUSES:\n{FRAMEWORK.as_prompt_block(task['clauses'])}",
    ]
    if task.get("previous_plan"):
        parts.append(
            f"\nPREVIOUS PLAN:\n{json.dumps(task['previous_plan'].__dict__, indent=2)}"
        )  #D
    if task.get("execution_feedback"):
        parts.append(f"\nEXECUTION FEEDBACK:\n{task['execution_feedback']}")  #E
    parts.append("\nProduce or revise the plan.")

    raw = llm_call(PLANNER_SYSTEM, "\n".join(parts), schema={"type": "object"})  #F
    try:
        return Plan(  #G
            focus_clauses=raw.get("focus_clauses", FRAMEWORK.all_ids()),
            evidence_emphasis=raw.get("evidence_emphasis", []),
            notes=raw.get("notes", ""),
        )
    except Exception:
        return Plan(
            focus_clauses=FRAMEWORK.all_ids(),
            evidence_emphasis=[],
            notes="default",
        )  #H
