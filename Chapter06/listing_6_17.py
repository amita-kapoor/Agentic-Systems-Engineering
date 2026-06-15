class ReportClause(BaseModel):
    """One assertion in the draft report, tied to a regulatory clause."""

    id: str
    claim: str
    evidence: str
    compliance_status: Literal["compliant", "non_compliant", "insufficient_information"]


class DraftReport(BaseModel):
    summary: str
    clauses: list[ReportClause]
    open_issues: list[str] = Field(default_factory=list)


class ValidationSignal(BaseModel):
    missing_clauses: list[str] = Field(default_factory=list)
    clauses_without_evidence: list[str] = Field(default_factory=list)
    unknown_clause_refs: list[str] = Field(default_factory=list)
    coverage_ratio: float = 0.0
    is_clean: bool = False


class RuleValidator:
    """Structural check. Now also verifies that 'compliant' claims cite required evidence."""

    MIN_EVIDENCE_LEN = 10

    def __init__(self, framework: RegulatoryFramework):
        self.framework = framework

    def validate(self, draft: DraftReport) -> ValidationSignal:
        all_required = set(self.framework.all_ids())
        addressed = {rc.id for rc in draft.clauses if rc.id in all_required}
        unknown = [rc.id for rc in draft.clauses if rc.id not in all_required]
        missing = sorted(all_required - addressed)
        no_evidence = [
            rc.id for rc in draft.clauses
            if rc.id in all_required and len(rc.evidence.strip()) < self.MIN_EVIDENCE_LEN
        ]  #A

        unsupported_compliant = []  #B
        for rc in draft.clauses:
            if rc.id not in all_required:
                continue
            if rc.compliance_status != "compliant":
                continue
            clause = self.framework.get(rc.id)
            if not clause or not clause.required_evidence:
                continue
            evidence_lower = rc.evidence.lower()
            cited = [
                key for key in clause.required_evidence
                if any(token in evidence_lower for token in key.lower().split("_"))
            ]
            if not cited:
                unsupported_compliant.append(rc.id)

        coverage = len(addressed) / max(len(all_required), 1)
        is_clean = (
            not missing and not no_evidence and not unknown and not unsupported_compliant
        )

        signal = ValidationSignal(
            missing_clauses=missing,
            clauses_without_evidence=no_evidence,
            unknown_clause_refs=unknown,
            coverage_ratio=round(coverage, 2),
            is_clean=is_clean,
        )
        signal.clauses_without_evidence = list(set(no_evidence + unsupported_compliant))  #C
        return signal


VALIDATOR = RuleValidator(FRAMEWORK)
