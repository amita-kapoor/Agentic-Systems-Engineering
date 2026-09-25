from enum import Enum
from typing import Any, Literal, Optional

from pydantic import BaseModel


class RiskLevel(str, Enum):
    LOW = "low"  # Read-only, no side effects - safe to retry freely
    MEDIUM = "medium"  # Reversible side effects - retry with idempotency key
    HIGH = "high"  # Irreversible side effects - log, alert, consider HITL
    CRITICAL = "critical"  # Financial, legal, or safety impact - HITL mandatory


class CustomerLookupInput(BaseModel):
    customer_id: str


class CustomerLookupOutput(BaseModel):  # Responsibility: Business outcome
    status: Literal["found", "not_found"]
    customer: Optional[dict] = None


class ActionResult(BaseModel):  # Responsibility: What happened during execution
    status: Literal[
        "success", "failure", "partial", "pending"
    ]  # pending means the action is awaiting human approval
    output: Optional[Any] = None
    error: Optional[dict] = None
    latency_ms: float = 0.0
