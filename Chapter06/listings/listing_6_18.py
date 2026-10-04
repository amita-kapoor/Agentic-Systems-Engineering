GENERATOR_SYSTEM = """You are a compliance analyst.
Given a product description, regulatory clauses, and any prior feedback,
produce a structured compliance report.

Return JSON matching exactly:
{
  "summary": string,
  "clauses": [
    {
      "id": string,
      "claim": string,
      "evidence": string,
      "compliance_status": "compliant" | "non_compliant" | "insufficient_information"
    }, ...
  ],
  "open_issues": [string, ...]
}

Rules:
- "id" must match one of the provided regulatory clause IDs. Address every clause.
- "claim" restates what the regulation requires.
- "evidence" cites specific facts from the product description. At least 10 characters.
- "compliance_status":
  "compliant" only when the product description provides concrete facts that satisfy the clause.
  "non_compliant" when the description shows the requirement is violated.
  "insufficient_information" when the description does not say enough to judge.
- Do NOT mark a clause "compliant" by inventing facts. If unsure, use "insufficient_information".
- "open_issues" must list every clause that is non_compliant or insufficient_information,
  written as a plain English sentence that names the clause ID. Example:
  "Data retention practices are not documented (REG-3)."
Do NOT use machine tags or @-syntax in open_issues.
"""  # System prompt defines the report schema and compliance rules


def generator(task: dict) -> DraftReport:
    rel_clauses = task["clauses"]
    parts = [  # Build the first-pass context from product facts, regulations, and memory
        f"PRODUCT DESCRIPTION:\n{task['product_description']}",
        f"\nREGULATORY CLAUSES:\n{FRAMEWORK.as_prompt_block(rel_clauses)}",
        f"\nPAST EXPERIENCE:\n{task['memory_block']}",
    ]
    if task.get("previous_draft"):
        prev = task["previous_draft"].model_dump()
        parts.append(
            f"\nPREVIOUS DRAFT:\n{json.dumps(prev, indent=2)}"
        )  # Include the previous draft on later reflection iterations
    if task.get("validator_signal"):
        parts.append(
            f"\nVALIDATOR SIGNAL:\n{json.dumps(task['validator_signal'].model_dump(), indent=2)}"
        )  # Include deterministic validator feedback when available
    if task.get("critique_feedback"):
        parts.append(f"\nCRITIQUE FEEDBACK:\n{task['critique_feedback']}")
    parts.append("\nDraft the report now.")  # Include evaluator feedback from the prior iteration

    raw = llm_call(
        GENERATOR_SYSTEM, "\n".join(parts), schema={"type": "object"}
    )  # Request structured JSON output from the model
    try:
        clauses = [
            ReportClause(**c) for c in raw.get("clauses", [])
        ]  # Parse model output into typed report objects
        return DraftReport(
            summary=raw.get("summary", ""),
            clauses=clauses,
            open_issues=raw.get("open_issues", []),
        )
    except Exception as e:
        return DraftReport(
            summary=f"[parse_error: {e}]", clauses=[], open_issues=[]
        )  # Return a safe parse-error report instead of crashing the loop
