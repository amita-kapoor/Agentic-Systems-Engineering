class CustomerLookupInput(BaseModel):
    customer_id: str


class CustomerLookupOutput(BaseModel):  #A
    status: Literal["found", "not_found"]
    customer: Optional[dict] = None


class ActionResult(BaseModel):  #B
    status: Literal["success", "failure", "partial", "pending"]  #C
    output: Optional[Any] = None
    error: Optional[dict] = None
    latency_ms: float = 0.0


#A Responsibility: Business outcome
#B Responsibility: What happened during execution
#C pending means the action is awaiting human approval.
