import subprocess
from typing import Literal

from pydantic import BaseModel

ALLOWED_COMMANDS = {"ls", "cat", "echo"}


class ShellCommandInput(BaseModel):
    command: str
    args: list[str] = []


class ShellCommandOutput(BaseModel):
    status: Literal["success", "failure"]
    returncode: int
    stdout: str
    stderr: str


class ShellCommandTool:
    metadata = ToolMetadata(
        name="shell_run_allowlisted",
        description="Run an allowlisted shell command with sanitized arguments.",
        args_schema=ShellCommandInput,
        risk_level=RiskLevel.HIGH,  # Shell execution is high risk
        is_idempotent=False,  # Commands may produce side effects
        timeout_seconds=5.0,  # Bound execution time
        requires_confirmation=True,  # Require explicit approval
    )

    async def execute(self, input: ShellCommandInput) -> ActionResult:
        if input.command not in ALLOWED_COMMANDS:  # Enforce allowlist
            return ActionResult(
                status="failure",
                error={"code": "CommandNotAllowed", "retryable": False},
            )

        result = subprocess.run(
            [input.command] + input.args,  # Structured args (no shell=True)
            capture_output=True,
            text=True,
            timeout=5,  # Hard timeout at execution level
        )

        return ActionResult(
            status="success",
            output=ShellCommandOutput(
                status="success",
                returncode=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
            ),
        )
