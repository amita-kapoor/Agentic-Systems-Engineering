from typing import cast


class CustomerLookupAdapterV1:
    metadata = ToolMetadata(
        name="get_customer_v1_compat",
        description="Compatibility wrapper for version 1 callers.",
        args_schema=CustomerLookupInputV1,
        version="1.0.0",
    )

    def __init__(self, v2_tool: CustomerLookupToolV2):
        self.v2_tool = v2_tool  # Underlying implementation

    async def execute(self, input: CustomerLookupInputV1) -> ActionResult:
        v2_input = CustomerLookupInputV2(
            customer_id=input.customer_id,
            include_orders=False,
        )
        result = await self.v2_tool.execute(v2_input)

        if result.status != "success":
            return result

        v2_output = cast(
            CustomerLookupResultV2, result.output
        )  # Cast required because ActionResult.output is untyped (Any)
        v1_output = CustomerLookupResultV1(
            status=v2_output.status,
            customer=v2_output.customer,
        )

        return ActionResult(
            status="success",
            output=v1_output,
            latency_ms=result.latency_ms,
        )
