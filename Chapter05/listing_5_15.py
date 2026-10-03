class IdempotentExecutor:
    def __init__(self, store):
        self.store = store

    async def execute(self, tool_name: str, params: dict, fn, operation_id: str) -> ActionResult:
        key = make_idempotency_key(tool_name, params, operation_id: str)

        cached = await self.store.get(key)
        if cached:
            return cached

        result = await fn()
        if result.status == "success": #A
            await self.store.set(key, result)

        return result


#A A success is a fact about the world that must not be repeated; a failure is a fact about one attempt
