from playwright.async_api import Page, Locator

from pages.base_page import BasePage


class CarDetailsPage(BasePage):
    def __init__(self, page: Page):
        self.page = page
        self.vrm_input: Locator = self.page.locator('#registration-number-input')
        self.find_car: Locator = self.page.locator('#find-vehicle-btn')
        # vehicle specifics
        self.reg_number: Locator = self.page.locator('#vehicleSummaryRegNumber>b')
        self.manufacturer: Locator = self.page.locator('.panel>p:nth-child(2)>b')
        self.model: Locator = self.page.locator('.panel>p:nth-child(3)>b')
        self.year: Locator = self.page.locator('.panel>p:nth-child(5)>b')

        self.change_vehicle_btn: Locator = self.page.locator('#change-vehicle-btn')
        self.error_msg: Locator = self.page.locator('#vehicle-error-container>.error-summary>.error-summary__heading')

    async def find_car_details(self, vrm):
        await self.vrm_input.fill(vrm)
        await self.find_car.click()

    async def get_error_msg(self):
        return await self.error_msg.is_visible()

    async def get_reg_number(self):
        return await self.reg_number.inner_text()

    async def get_make_model(self):
        car_manufacturer = await self.manufacturer.inner_text()
        car_model = await self.model.inner_text()
        make_model = car_manufacturer + " " + car_model
        return make_model

    async def get_year(self):
        return await self.year.inner_text()

    async def click_change_vehicle(self):
        await self.change_vehicle_btn.click()
