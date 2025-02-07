from playwright.async_api import Page, Locator

from pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page: Page):
        self.page = page
        self.get_car_quote: Locator = self.page.locator('[data-mi-click-label="homepage-hero-car-insurance-GAQ"]')
        self.accept_cookies: Locator = self.page.locator('#button-save-all')

    async def get_quote(self):
        await self.accept_cookies.click()
        await self.get_car_quote.click()

    async def click_car_quote(self):
        await self.get_car_quote.click()