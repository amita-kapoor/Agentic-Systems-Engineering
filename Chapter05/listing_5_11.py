class IdempotentExecutor:
    def __init__(self, store):
        self.store = store

    async def execute(self, tool_name, params, operation_id):
        key = make_idempotency_key(tool_name, params, operation_id)

        cached = await self.store.get(key)
        if cached:
            return cached

        result = await self._execute(tool_name, params)  #A
        if result.status == "success": #B
             await self.store.set(key, result)


        return result

#A _execute stands for the tool call itself 
#B Cache successes only.
