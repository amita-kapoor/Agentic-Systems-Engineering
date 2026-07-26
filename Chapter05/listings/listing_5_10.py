import hashlib
import json


def make_idempotency_key(tool_name: str, inputs: dict) -> str:
    canonical = json.dumps(
        {"tool": tool_name, "inputs": inputs},
        sort_keys=True,
    )
    return hashlib.sha256(canonical.encode()).hexdigest()
