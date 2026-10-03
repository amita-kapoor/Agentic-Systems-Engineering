class SafeExecutor:
    """Sequences policy check -> idempotent execution -> circuit breaker."""

    def __init__(self, store, circuit_breaker: CircuitBreaker):
        self.gate = PolicyGate()
        self.idempotent = IdempotentExecutor(store)
        self.breaker = circuit_breaker

    async def execute(
        self,
        tool: "BaseTool",
        inputs: dict,
    ) -> ActionResult:
        #A
        decision = self.gate.check(tool)

        if decision == PolicyDecision.BLOCK:
            return ActionResult(
                status="failure",
                error={"code": "PolicyBlocked", "message": "Blocked by policy", "retryable": False},
            )

        if decision == PolicyDecision.REQUIRE_APPROVAL:
            return ActionResult(
                status="pending",
                error={"code": "AwaitingApproval", "message": "Awaiting human approval", "retryable": False},
            )

        
        try: #B
            validated = tool.metadata.args_schema(**inputs)
        except ValidationError as e:
            return ActionResult(
                status="failure",
                error={"code": "InvalidInput", "message": str(e), "retryable": False},
            )

        async def _call(): #C
            return await tool.execute(validated)

        try:
            return await self.idempotent.execute(
                tool_name=tool.metadata.name,
                params=inputs,
                fn=lambda: self.breaker.call(_call),
                operation_id=operation_id,
            )
        except CircuitOpenError as e: #D
            return ActionResult(
                status="failure",
                error={"code": "CircuitOpen", "message": str(e), "retryable": True},
            )
        except Exception as e:
            return ActionResult(
                status="failure",
                error={"code": type(e).__name__, "message": str(e),
                       "retryable": isinstance(e, (ConnectionError, TimeoutError))},
            )



#A Stage 1: policy gate
#B Validation is the caller's problem, so it must not count against the dependency's circuit 
#C The breaker sits inside the idempotency wrapper, so it sees only real execution attempts 
#D An open circuit comes back as a structured failure the caller may retry
