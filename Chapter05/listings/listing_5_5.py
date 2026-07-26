class WireTransferInput(BaseModel):
    account_number: str
    amount_usd: float
    recipient_name: str


# This will raise a validation error at definition time
class InitiateWireTransferTool:
    metadata = ToolMetadata(
        name="initiate_wire_transfer",
        description="Transfer funds to an external bank account.",
        args_schema=WireTransferInput,
        # Raises ValueError: CRITICAL tools must require confirmation
        risk_level=RiskLevel.CRITICAL,
        requires_confirmation=False,  # Violates policy
    )
