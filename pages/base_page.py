from playwright.async_api import Page
from requests import Response
from config import NETWORK_IDLE


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    async def navigate(self, url: str) -> Response:
        print(f"DEBUG: Navigating to {url}")
        print(f"DEBUG: Page type: {type(self.page)}")
        if self.page.is_closed():
            raise RuntimeError("Page is already closed before navigation")
        await self.page.goto(url, wait_until=NETWORK_IDLE)