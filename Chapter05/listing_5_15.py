class IdempotentExecutor:
    def __init__(self, store):
        self.store = store

    async def execute(self, tool_name: str, params: dict, fn) -> ActionResult:
        key = make_idempotency_key(tool_name, params)

        cached = await self.store.get(key)
        if cached:
            return cached

        result = await fn()
        await self.store.set(key, result)

        return result
