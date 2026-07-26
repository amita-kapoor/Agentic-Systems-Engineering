class RegulatoryClause(BaseModel):
    """A single regulatory requirement. Lives in semantic memory."""

    id: str
    title: str
    text: str
    required_evidence: list[str] = Field(default_factory=list)


class RegulatoryFramework:
    """Semantic memory for regulatory rules. Stable across tasks."""

    def __init__(self, clauses: list[RegulatoryClause]):
        self._clauses = {c.id: c for c in clauses}

    def get(self, clause_id: str) -> Optional[RegulatoryClause]:
        return self._clauses.get(clause_id)

    def all_ids(self) -> list[str]:
        return list(self._clauses.keys())

    def retrieve_relevant(self, product_description: str) -> list[RegulatoryClause]:
        """Stand-in for staged retrieval. Returns all clauses for this small example."""
        return list(self._clauses.values())

    def as_prompt_block(self, clauses: list[RegulatoryClause]) -> str:
        lines = []
        for c in clauses:
            evidence = ", ".join(c.required_evidence) or "none"
            lines.append(f"[{c.id}] {c.title}: {c.text} (required evidence: {evidence})")
        return "\n".join(lines)


FRAMEWORK = RegulatoryFramework(
    [  # A small synthetic framework for a hypothetical "Customer Payment Data Directive"
        RegulatoryClause(
            id="REG-1",
            title="Encryption at rest",
            text=(
                "Customer payment data must be encrypted at rest using an industry-standard cipher."
            ),
            required_evidence=["cipher_name", "key_management_policy"],
        ),
        RegulatoryClause(
            id="REG-2",
            title="Access logging",
            text="All access to payment data must be logged with user identity and timestamp.",
            required_evidence=["log_destination", "retention_period"],
        ),
        RegulatoryClause(
            id="REG-3",
            title="Data retention",
            text="Payment data must not be retained beyond 90 days unless explicitly justified.",
            required_evidence=["retention_period", "justification_if_exceeded"],
        ),
        RegulatoryClause(
            id="REG-4",
            title="Cross-border transfer",
            text="Cross-border transfers of payment data require a documented legal basis.",
            required_evidence=["transfer_destinations", "legal_basis"],
        ),
    ]
)

print("Framework loaded. Clause IDs:", FRAMEWORK.all_ids())
