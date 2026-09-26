import asyncio
import time
from enum import Enum
from typing import Any, Literal, Optional, Type

from pydantic import BaseModel, Field, model_validator

class RiskLevel(str, Enum): #A
    LOW      = "low"       #B
    MEDIUM   = "medium"    #C
    HIGH     = "high"      #D
    CRITICAL = "critical"  #E


class ToolMetadata(BaseModel):  #F
    name: str
    description: str
    args_schema: Type[BaseModel]
    risk_level: RiskLevel = RiskLevel.LOW
    is_idempotent: bool = True
    timeout_seconds: float = 5.0
    cost_estimate_usd: Optional[float] = None
    requires_confirmation: bool = False
    preconditions: list[str] = Field(default_factory=list)
    postconditions: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def enforce_confirmation_for_critical(self) -> "ToolMetadata":
        if self.risk_level == RiskLevel.CRITICAL and not self.requires_confirmation:
            raise ValueError(
                f"Tool '{self.name}' is CRITICAL risk but requires_confirmation=False. "

                "CRITICAL tools must require human confirmation."
            )
        return self
#A Defined first, because ToolMetadata uses it as a default value 
#B Read-only with no side effects, so safe to retry freely 
#C Reversible side effects; retry with an idempotency key 
#D Irreversible side effects; log, alert, and consider human review 
#E Financial, legal, or safety impact; human review is mandatory 
#F Responsibility: how the tool should be treated
