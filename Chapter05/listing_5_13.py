class AgentSaga:
    def __init__(self):
        self.compensations = []

    async def execute_step(self, action, compensate):
        result = await action()
        self.compensations.append(compensate)
        return result

    async def rollback(self):
        while self.compensations:
            compensate = self.compensations.pop()
            await compensate()
