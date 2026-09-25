class IdempotentExecutor:
    def __init__(self, store):
        self.store = store

    async def execute(self, tool_name, params):
        key = make_idempotency_key(tool_name, params)

        cached = await self.store.get(key)
        if cached:
            return cached

        result = await self._execute(tool_name, params)
        await self.store.set(key, result)

        return result
