import time


class CircuitBreaker:
    def __init__(self, failure_threshold=5, reset_timeout_s=60):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout_s
        self.failures = 0
        self.state = "CLOSED"  # Closed state: requests flow normally
        self.last_failure_time = 0.0

    async def call(self, tool_fn, *args, **kwargs):
        if self.state == "OPEN":  # Open state: requests are blocked
            if time.monotonic() - self.last_failure_time > self.reset_timeout:
                self.state = "HALF_OPEN"  # Half-open state: allow limited test requests
            else:
                raise RuntimeError("Circuit open - dependency unavailable")

        try:
            result = await tool_fn(*args, **kwargs)

            if self.state == "HALF_OPEN":
                self.state = "CLOSED"  # Successful probe resets the circuit
                self.failures = 0

            return result

        except Exception:
            self.failures += 1
            self.last_failure_time = time.monotonic()

            if self.failures >= self.failure_threshold:
                self.state = "OPEN"  # Failure threshold triggers open state
            raise
