class Critique(TypedDict):
    status: Literal["acceptable", "needs_revision", "converged"]
    issues: list[str]
    feedback: str


CITABLE_FIELDS = {
    "summary",
    "clauses",
    "open_issues",
}  # A whitelist of fields a blocker is allowed to cite. Anything else is treated as a suggestion

BLOCKER_RULES = {  # A whitelist of rule names. Maps to the same four blocker categories from before
    "evidence_status_mismatch",  # Status contradicts evidence
    "summary_misrepresents",  # Summary contradicts per-clause statuses
    "open_issues_incomplete",  # Open_issues missing a non_compliant or insufficient clause
    "factual_error",  # Contradicts product description or clause text
}


CRITIC_SYSTEM = f"""You are a senior compliance reviewer.
You output structured blockers. A blocker has three required fields: a rule name, the
field in the report it concerns, and a one-sentence description.

Allowed rule names: {sorted(BLOCKER_RULES)}
Allowed field names: {sorted(CITABLE_FIELDS)}

Return JSON matching exactly:
{{
  "blockers": [
    {{"rule": string, "field": string, "description": string}}, ...
  ],
  "suggestions": [string, ...]
}}

Important rules of engagement:
- An empty "blockers" list is a normal, valid, frequently correct outcome.
  When the report is honest and the per-clause statuses match their evidence,
  return zero blockers. Do not invent issues.
- Only the four rule names above count as blockers. Anything else (style,
  thoroughness, suggested rewordings, additional caveats) goes in "suggestions".
- The "open_issues_incomplete" rule fires only when a clause whose
  compliance_status is "non_compliant" or "insufficient_information" is missing
  from open_issues. A "compliant" clause should NOT appear in open_issues.
- The "summary_misrepresents" rule fires only when the summary makes a claim
  directly contradicted by the per-clause statuses. A summary that honestly
  acknowledges both compliant and non-compliant clauses is not a misrepresentation.
"""


def _filter_blockers(raw_blockers: list[dict]) -> list[dict]:
    """Drop anything that doesn't cite a known rule and a known field."""
    clean = []
    for b in raw_blockers:
        if not isinstance(b, dict):
            continue
        rule = b.get("rule", "")
        field = b.get("field", "")
        if rule in BLOCKER_RULES and field in CITABLE_FIELDS:
            clean.append(b)
    return clean


def critic(task: dict, draft: DraftReport, signal: ValidationSignal) -> Critique:
    user_prompt = (
        f"REGULATORY CLAUSES:\n{FRAMEWORK.as_prompt_block(task['clauses'])}\n\n"
        f"DRAFT REPORT:\n{json.dumps(draft.model_dump(), indent=2)}\n\n"
        f"VALIDATOR SIGNAL:\n{json.dumps(signal.model_dump(), indent=2)}\n\n"
        f"Identify blocking issues. Empty list is a valid response."
    )
    raw = llm_call(CRITIC_SYSTEM, user_prompt, schema={"type": "object"})
    raw_blockers = raw.get("blockers", []) or []
    suggestions = raw.get("suggestions", []) or []
    blockers = _filter_blockers(raw_blockers)

    if signal.is_clean and not blockers:
        return Critique(
            status="acceptable",
            issues=[],
            feedback="No blockers."
            if not suggestions
            else "Suggestions: " + "; ".join(suggestions),
        )

    if not signal.is_clean:
        feedback = (
            f"Structural issues. Missing: {signal.missing_clauses}. "
            f"Without evidence: {signal.clauses_without_evidence}."
        )
    else:
        feedback = "Blockers: " + "; ".join(
            f"[{b['rule']}@{b['field']}] {b['description']}" for b in blockers
        )

    return Critique(
        status="needs_revision",
        issues=[f"{b['rule']}@{b['field']}" for b in blockers],
        feedback=feedback,
    )
