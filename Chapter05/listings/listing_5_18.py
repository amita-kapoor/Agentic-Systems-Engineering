import asyncio


class InMemoryStore:
    """In-memory store for demonstration.

    Replace with Redis or Postgres in production.
    """

    def __init__(self):
        self._data = {}

    async def get(self, key):
        return self._data.get(key)

    async def set(self, key, value):
        self._data[key] = value


async def demo():
    registry = ToolRegistry()
    registry.register(CustomerLookupTool())

    store = InMemoryStore()
    breaker = CircuitBreaker(failure_threshold=3, reset_timeout_s=30)

    executor = SafeExecutor(store=store, circuit_breaker=breaker)
    engine = ActionEngine(registry=registry, executor=executor)

    # Stage 1: candidate retrieval
    candidates = engine.get_candidates(
        query="look up customer account information",
        max_risk=RiskLevel.MEDIUM,
    )
    print(f"Candidates: {[t.metadata.name for t in candidates]}")

    # Stage 2: model selects tool (simulated here)
    result = await engine.run(
        tool_name="get_customer",
        inputs={"customer_id": "cust_1"},
    )

    print(f"Execution status: {result.status}")
    print(f"Domain outcome:   {result.output.status}")
    print(f"Customer:         {result.output.customer}")


asyncio.run(demo())
