import asyncio
import time


class CustomerLookupTool:
    metadata = ToolMetadata(
        name="get_customer",
        description="Retrieve a customer record by unique identifier.",
        args_schema=CustomerLookupInput,
        risk_level=RiskLevel.LOW,
        is_idempotent=True,
        timeout_seconds=2.0,
        requires_confirmation=False,
        postconditions=["customer record available in context"],
    )

    async def execute(self, input: CustomerLookupInput) -> ActionResult:
        start = time.monotonic()
        try:
            result = await asyncio.wait_for(
                self._run(input),
                timeout=self.metadata.timeout_seconds,
            )
            return ActionResult(
                status="success",
                output=result,
                latency_ms=(time.monotonic() - start) * 1000,
            )
        except asyncio.TimeoutError:
            return ActionResult(
                status="failure",
                error={
                    "code": "TimeoutError",
                    "message": "Tool execution timed out",
                    "retryable": True,
                },
                latency_ms=self.metadata.timeout_seconds * 1000,
            )

    async def _run(self, input: CustomerLookupInput) -> CustomerLookupOutput:
        # In production this would be: record = await db.get(input.customer_id)
        database = {"cust_1": {"name": "Asha Gupta", "email": "asha@example.com"}}
        record = database.get(input.customer_id)
        if record is None:
            return CustomerLookupOutput(status="not_found")
        return CustomerLookupOutput(status="found", customer=record)
