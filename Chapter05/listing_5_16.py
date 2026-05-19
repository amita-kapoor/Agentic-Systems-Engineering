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
        # Stage 1: policy gate
        decision = self.gate.check(tool)

        if decision == PolicyDecision.BLOCK:
            return ActionResult(
                status="failure",
                error={"code": "PolicyBlocked", "retryable": False},
            )

        if decision == PolicyDecision.REQUIRE_APPROVAL:
            return ActionResult(
                status="pending",
                error={"code": "AwaitingApproval", "retryable": False},
            )

        # Stage 2: validated execution through safeguards
        async def _call():
            validated = tool.metadata.args_schema(**inputs)
            return await tool.execute(validated)

        return await self.idempotent.execute(
            tool_name=tool.metadata.name,
            params=inputs,
            fn=lambda: self.breaker.call(_call),
        )
