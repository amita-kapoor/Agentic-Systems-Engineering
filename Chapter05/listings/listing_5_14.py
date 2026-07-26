from enum import Enum


class PolicyDecision(str, Enum):
    ALLOW = "allow"
    REQUIRE_APPROVAL = "require_approval"
    BLOCK = "block"


class PolicyGate:
    """Reads tool metadata and returns an execution decision."""

    def check(self, tool: "BaseTool") -> PolicyDecision:
        risk = tool.metadata.risk_level

        if risk == RiskLevel.CRITICAL:
            return PolicyDecision.REQUIRE_APPROVAL

        if risk == RiskLevel.HIGH and tool.metadata.requires_confirmation:
            return PolicyDecision.REQUIRE_APPROVAL

        return PolicyDecision.ALLOW
