from playwright.async_api import async_playwright
from pydantic import BaseModel
from typing import Literal, Optional
from playwright.async_api import async_playwright


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
        risk_level=RiskLevel.MEDIUM,
        is_idempotent=True,
        timeout_seconds=10.0,
        requires_confirmation=False,
    )

    async def execute(self, input: BrowserReadInput) -> ActionResult:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(input.url)
            content = await page.inner_text("body")
            await browser.close()

        return ActionResult(
            status="success",
            output=BrowserReadOutput(status="success", content=content),
        )
