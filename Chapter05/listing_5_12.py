import time
import asyncio

class CircuitOpenError(RuntimeError): #A
    """Raised when the circuit rejects a call without attempting it."""


class CircuitBreaker:
    def __init__(self, failure_threshold=5, reset_timeout_s=60):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout_s
        self.failures = 0
        self.state = "CLOSED"  #B
        self.last_failure_time = 0.0
        self._probe_lock = asyncio.Lock() #C


    async def call(self, tool_fn, *args, **kwargs):
        if self.state == "OPEN":  #D
            if time.monotonic() - self.last_failure_time > self.reset_timeout:
                self.state = "HALF_OPEN"  
            else:
                raise CircuitOpenError("Circuit open - dependency unavailable")

        if self.state == "HALF_OPEN": #E
            if self._probe_lock.locked():
                raise CircuitOpenError("Circuit half-open — probe already in flight")
            async with self._probe_lock:
                return await self._attempt(tool_fn, *args, **kwargs)

        return await self._attempt(tool_fn, *args, **kwargs)

    async def _attempt(self, tool_fn, *args, **kwargs):
        try:
            result = await tool_fn(*args, **kwargs)
        except Exception:
            self._record_failure()
            raise
        if self._is_dependency_failure(result): #F
            self._record_failure()
            return result
        self.state = "CLOSED" #G
        self.failures = 0
        return result

    @staticmethod
    def _is_dependency_failure(result) -> bool: #H
        return (
            getattr(result, "status", None) == "failure"
            and (getattr(result, "error", None) or {}).get("retryable") is True
        )

    def _record_failure(self):
        self.failures += 1
        self.last_failure_time = time.monotonic()
        if self.state == "HALF_OPEN" or self.failures >= self.failure_threshold:
            self.state = "OPEN"  #I


#A Distinguishes a call the circuit rejected from one that failed
#B Closed state: requests flow normally
#C Only one probe may run while half-open
#D Open state: requests are are rejected until the cooldown passesblocked
#E Half-open state: exactly one test requestallow limited test requests
#F A returned failure counts, because this is how the tools report a timeout
#G Successful probe closes the circuit resets the countcircuit
#H Only a retryable failure means the dependency is unwell. A validation error is the caller's fault. 
#I A failed probe reopens the circuit at onceFailure threshold triggers open state

