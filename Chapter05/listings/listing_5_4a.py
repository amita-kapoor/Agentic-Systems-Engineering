from typing import Optional, Type

from pydantic import BaseModel, Field, model_validator


class ToolMetadata(BaseModel):  # Responsibility: How the tool should be treated
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
