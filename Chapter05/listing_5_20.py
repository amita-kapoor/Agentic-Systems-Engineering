import subprocess
from typing import Literal, Optional
from pathlib import Path
from pydantic import BaseModel


ALLOWED_COMMANDS = {"ls", "cat", "echo"}
WORKSPACE = Path("/tmp/agent_workspace").resolve() #A
WORKSPACE.mkdir(parents=True, exist_ok=True)

class ShellCommandInput(BaseModel):
    command: str
    args: list[str] = []


class ShellCommandOutput(BaseModel):
    status: Literal["success", "failure"]
    returncode: int
    stdout: str
    stderr: str

   def rejection_reason(input: ShellCommandInput) -> Optional[str]:
    if input.command not in ALLOWED_COMMANDS: #B
        return "CommandNotAllowed"
    for arg in input.args:
        if arg.startswith("-"):
            continue
        if not (WORKSPACE / arg).resolve().is_relative_to(WORKSPACE): #C
            return "PathOutsideWorkspace"
    return None



class ShellCommandTool:
    metadata = ToolMetadata(
        name="shell_run_allowlisted",
        description="Run an allowlisted shell command inside the agent workspace.",
        args_schema=ShellCommandInput,
        risk_level=RiskLevel.HIGH,  #D
        is_idempotent=False,  
        timeout_seconds=5.0,  
        requires_confirmation=True,  
    )

    async def execute(self, input: ShellCommandInput) -> ActionResult:
        reason = rejection_reason(input)
        if reason:
            return ActionResult(
                status="failure",
                error={"code": reason, "message": f"{input.command} {input.args}", "retryable": False},
            )
        return await super().execute(input)

    async def _run(self, input: ShellCommandInput) -> ShellCommandOutput:
        try:
            result = await asyncio.to_thread(
                subprocess.run,
                [input.command] + input.args,  #E
                capture_output=True,
                text=True,
                timeout=self.metadata.timeout_seconds,
                cwd=WORKSPACE,
            )
        except subprocess.TimeoutExpired:
            raise asyncio.TimeoutError() #F

        return ShellCommandOutput(
            status="success" if result.returncode == 0 else "failure", #G
            returncode=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
        )


#A Every path argument must resolve inside this directory 
#B Enforces the command allowlist 
#C Rejects absolute paths, ../ traversal, and symlinks that lead outside the workspace 
#D Shell execution is high risk 
#E Structured arguments; no shell=True 
#F BaseTool turns this into a retryable failure
#G The command ran, so execution succeeded
