from playwright.async_api import async_playwright
from pydantic import BaseModel
from typing import Literal, Optional

ALLOWED_DOMAINS = {"example.com"} #A

class BrowserReadInput(BaseModel):
    url: str


class BrowserReadOutput(BaseModel):
    status: Literal["success", "failure"]
    content: Optional[str] = None


class BrowserReadTool:
    metadata = ToolMetadata(
        name="browser_read_page",
        description="Load a web page and extract visible text.",
        args_schema=BrowserReadInput,
        risk_level=RiskLevel.HIGH,  #B
        is_idempotent=True,
        timeout_seconds=10.0,
        requires_confirmation=False,
    )

    async def execute(self, input: BrowserReadInput) -> ActionResult:
        parsed = urlparse(input.url)
        host = (parsed.hostname or "").lower()
        allowed = any(host == d or host.endswith("." + d) for d in ALLOWED_DOMAINS)
        if parsed.scheme != "https" or not allowed: #C
            return ActionResult(
                status="failure",
                error={"code": "DomainNotAllowed", "message": input.url, "retryable": False},
            )
        return await super().execute(input) #D

    async def _run(self, input: BrowserReadInput) -> BrowserReadOutput:
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            try:
                page = await browser.new_page()
                await page.goto(input.url)
                content = await page.inner_text("body")
            finally:
                await browser.close() #E
        return BrowserReadOutput(status="success", content=content[:500]) #F
#A Only these domains may be loaded 
#B Page content is unstable and may contain injected instructions, so a person reviews each use 
#C Rejects plain HTTP, internal addresses, and lookalike domains before any browser starts 
#D BaseTool enforces timeout_seconds 
#E The browser closes even if navigation fails 
#F Capped, because this text goes into the model's context
