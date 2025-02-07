import pytest
from playwright.async_api import async_playwright, Page
from config import BASE_URL, BROWSER_HEADLESS, INPUT_FILE, OUTPUT_FILE
from pages.home_page import HomePage
from contextlib import asynccontextmanager
import re
import csv
import aiofiles
import asyncio

from pages.car_details_page import CarDetailsPage


@pytest.fixture(scope="session")
async def base_url():
    return BASE_URL

@pytest.fixture(scope="session")
def input_file_path():
    return INPUT_FILE

@pytest.fixture(scope="session")
def output_file_path():
    return OUTPUT_FILE

@asynccontextmanager
@pytest.fixture(scope='function')
async def chromium_page():
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=BROWSER_HEADLESS, slow_mo=2000)
        context = await browser.new_context()
        page = await context.new_page()
        yield page
        await page.close()
        await context.close()
        await browser.close()
        await playwright.stop()

@pytest.fixture(scope="function")
async def home_page(chromium_page: Page) -> HomePage:
    print(f"DEBUG: chromium_page type: {type(chromium_page)}")
    return HomePage(chromium_page)

@pytest.fixture(scope="function")
async def car_details_page(chromium_page: Page) -> CarDetailsPage:
    print(f"DEBUG: chromium_page type: {type(chromium_page)}")
    return CarDetailsPage(chromium_page)


# Async function to read VRMs from a file
@pytest.fixture(scope='session')
async def read_vrms_from_file(input_file_path):
    pattern = r'\b[A-Z]{2}\d{2}\s?[A-Z]{3}\b'  # UK VRM format
    async with aiofiles.open(input_file_path, 'r') as file:
        content = await file.read()  # Asynchronously read the file content
        print(f"Debugging: File '{input_file_path}' opened successfully")
        vrms = re.findall(pattern, content)
        print(f"Found VRMs: {vrms}")
    return vrms

# Async function to read data from the output text file
@pytest.fixture(scope='session')
async def read_vehicle_specifics(output_file_path):
    vehicle_data = []
    async with aiofiles.open(output_file_path, 'r') as file:
        content = await file.read()
        csv_reader = csv.DictReader(content.splitlines())
        for row in csv_reader:
            vehicle_data.append((row['VARIANT_REG'], row['MAKE_MODEL'], row['YEAR']))
    return vehicle_data








