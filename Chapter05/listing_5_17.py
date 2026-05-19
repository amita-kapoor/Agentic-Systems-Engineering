class ActionEngine:
    """Top-level coordinator for the action pipeline."""

    def __init__(self, registry: ToolRegistry, executor: SafeExecutor):
        self.registry = registry
        self.executor = executor

    def get_candidates(
        self,
        query: str,
        max_risk: RiskLevel = RiskLevel.HIGH,
    ):
        return self.registry.search(query, top_k=5, max_risk=max_risk)

    async def run(
        self,
        tool_name: str,
        inputs: dict,
    ) -> ActionResult:
        tool = self.registry.get(tool_name)

        if tool is None:
            return ActionResult(
                status="failure",
                error={
                    "code": "ToolNotFound",
                    "message": f"No tool named '{tool_name}'",
                    "retryable": False,
                },
            )

        return await self.executor.execute(tool, inputs)
