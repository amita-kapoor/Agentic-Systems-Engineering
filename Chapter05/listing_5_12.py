import time


class CircuitBreaker:
    def __init__(self, failure_threshold=5, reset_timeout_s=60):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout_s
        self.failures = 0
        self.state = "CLOSED"  #A
        self.last_failure_time = 0.0

    async def call(self, tool_fn, *args, **kwargs):
        if self.state == "OPEN":  #B
            if time.monotonic() - self.last_failure_time > self.reset_timeout:
                self.state = "HALF_OPEN"  #C
            else:
                raise RuntimeError("Circuit open - dependency unavailable")

        try:
            result = await tool_fn(*args, **kwargs)

            if self.state == "HALF_OPEN":
                self.state = "CLOSED"  #D
                self.failures = 0

            return result

        except Exception:
            self.failures += 1
            self.last_failure_time = time.monotonic()

            if self.failures >= self.failure_threshold:
                self.state = "OPEN"  #E
            raise
