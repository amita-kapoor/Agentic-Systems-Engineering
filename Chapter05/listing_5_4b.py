from enum import Enum
from typing import Any, Literal, Optional

from pydantic import BaseModel


class RiskLevel(str, Enum):
    LOW = "low"  #A
    MEDIUM = "medium"  #B
    HIGH = "high"  #C
    CRITICAL = "critical"  #D


class CustomerLookupInput(BaseModel):
    customer_id: str


class CustomerLookupOutput(BaseModel):  #E
    status: Literal["found", "not_found"]
    customer: Optional[dict] = None


class ActionResult(BaseModel):  #F
    status: Literal["success", "failure", "partial", "pending"]  #G
    output: Optional[Any] = None
    error: Optional[dict] = None
    latency_ms: float = 0.0


#A Read-only, no side effects - safe to retry freely
#B Reversible side effects - retry with idempotency key
#C Irreversible side effects - log, alert, consider HITL
#D Financial, legal, or safety impact - HITL mandatory
#E Responsibility: Business outcome
#F Responsibility: What happened during execution
#G pending means the action is awaiting human approval.
