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
        risk_level=RiskLevel.CRITICAL,  #A
        requires_confirmation=False,  #B
    )
