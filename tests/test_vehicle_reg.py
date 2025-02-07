import pytest
from playwright.async_api import async_playwright
import re
from pages.home_page import HomePage
from pages.car_details_page import CarDetailsPage
from conftest import base_url, read_vrms_from_file, read_vehicle_specifics
import aiofiles
import asyncio
from config import OUTPUT_FILE


class TestVehicleReg:
    @pytest.mark.asyncio
    # @pytest.mark.parametrize("variant_reg, make_model, year", asyncio.run(read_vehicle_specifics(OUTPUT_FILE)))
    async def test_search_vehicle_reg(self, home_page, car_details_page, base_url, read_vrms_from_file,
                                      read_vehicle_specifics) -> None:
        vrms = read_vrms_from_file
        print(f"VRMS List: {vrms}")
        vehicle_data_list = read_vehicle_specifics
        await home_page.navigate(base_url)
        await home_page.get_quote()
        for vrm in vrms:
            await car_details_page.find_car_details(vrm)
            if not await car_details_page.get_error_msg():
                for variant_reg, make_model, year in vehicle_data_list:
                    car_details_vrm = await car_details_page.get_reg_number()
                    print(f"Car details VRM: {car_details_vrm.replace(' ', '')}")
                    print(f"Variant reg: {variant_reg.replace(' ', '')}")
                    if car_details_vrm == variant_reg:
                        print(f"VRM: {vrm}")
                        car_details_model = await car_details_page.get_make_model()
                        car_details_year = await car_details_page.get_year()
                        print(f"VRM from car Details Page: {car_details_vrm}")

                        print(f"Testing VRM: {variant_reg}, Model: {make_model}, Year: {year}")
                        assert variant_reg == car_details_vrm, f"UI VRM '{car_details_vrm}' does not match file VRM '{variant_reg}'"
                        assert make_model.lower() == car_details_model.lower(), f"UI Model '{car_details_model}' does not match file Model '{make_model}'"
                        assert year == car_details_year, f"UI Model '{car_details_year}' does not match file Model '{year}'"
            else:
                print("Invalid Reg Number,trying again..")
            await home_page.navigate(base_url)
            await home_page.click_car_quote()
            #await car_details_page.click_change_vehicle()

