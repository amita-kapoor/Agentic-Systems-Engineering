import hashlib
import json


def make_idempotency_key(tool_name: str, inputs: dict) -> str:
    canonical = json.dumps(
        {"tool": tool_name, "inputs": inputs, "op": operation_id},  #A
        sort_keys=True,
    )
    return hashlib.sha256(canonical.encode()).hexdigest()

#A Operation id is created once, by the caller, when the agent decides to act, and reused on every retry of that one operation.
