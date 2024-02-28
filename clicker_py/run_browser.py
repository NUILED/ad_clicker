from playwright_recaptcha import recaptchav2
from playwright.async_api import async_playwright, TimeoutError
import random
from .exceptions import Captcha_not_solved 
import time
from . import config as configs
from .utility import *
import asyncio

target_texts = ["Acceptă tot", "Alles accepteren", "Alle akzeptieren", "Tout accepter", "Accept all","Godkänn alla"]

async def captcha_solve(page):
    async with recaptchav2.AsyncSolver(page) as solver:
        token = await solver.solve_recaptcha(wait=True)
        if token:
            print("Captcha solved")
        else:
            raise Captcha_not_solved

async def is_captcha_page(page):
    return await page.query_selector('.g-recaptcha') is not None

async def click_button_with_text(page, content):
    page_content = content
    for target_text in target_texts:
        if target_text in page_content:
            print("Found button with text:", target_text)
            button = await page.locator(f'button:has-text("{target_text}")').first()
            await button.click()

async def try_click(page, target1, target):
    divs = await page.query_selector_all("div[data-text-ad]")
    for div in divs:
        try:
            a = await div.query_selector("a")
            href = await a.get_attribute("href")
            print(href)
        except:
            print("No link found")
        # You may uncomment the following lines if you want to click on the link
        # if (href == target1) or (href == target):
        try:
            await a.click()
        except Exception as e:
            print(e)

        await page.wait_for_load_state("load")
        
        if await is_captcha_page(page):
            try:
                await captcha_solve(page)
            except Exception as e:
                raise e
        await asyncio.sleep(random.randint(8, 20))
        await page.evaluate('window.scrollBy(0, window.innerHeight);')

class BrowserHandler:
    def __init__(self, language, keywords, z, v):
        self.language = language
        self.keywords = keywords
    
    async def firstopen(self, page):
        await page.goto("https://www.whoer.net/")
        await asyncio.sleep(random.randint(2, 5))
        await page.wait_for_load_state("load")
        await page.goto("https://www.google.com/search?q=atm+near+me")
        await asyncio.sleep(random.randint(2, 5))
        await page.wait_for_load_state("load")
        if await is_captcha_page(page):
            try:
                await captcha_solve(page)
            except Exception as e:
                raise e
        await asyncio.sleep(random.randint(2, 5))
        content = await page.content()
        await click_button_with_text(page,content)
        await page.reload()

    async def secondopen(self, page):
        for keyword in self.keywords:
            search_url = f"https://www.google.com/search?q={keyword}"
            await asyncio.sleep(random.randint(3, 6))
            await page.wait_for_load_state("load")
            if await is_captcha_page(page):
                try:
                    await captcha_solve(page)
                except Exception as e:
                    raise e
            await page.goto(search_url)
            await asyncio.sleep(random.randint(2, 5))
            await page.wait_for_load_state("load")
            divs = await page.query_selector_all("div[data-text-ad]")
            try:
                await try_click(page, configs.target , configs.target1)
            except Exception as e:
                raise e

    async def configure_browser_context(self, browser):
        context = await browser.new_context(
            extra_http_headers = {"Accept-Language": configs.language},
            geolocation={
                "latitude": random.uniform(configs.casablanca_bounds["latitude_min"], configs.casablanca_bounds["latitude_max"]),
                "longitude": random.uniform(configs.casablanca_bounds["longitude_min"], configs.casablanca_bounds["longitude_max"])
            },
            permissions=["geolocation"]
        )
        user_agent = random.choice(configs.Agent)
        await context.route("**/tel/*", lambda route: route.continue_())
        await context.set_extra_http_headers(headers={"User-Agent": user_agent})
        return context

    async def run_browser(self):
        await asyncio.sleep(random.randint(2, 6))
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=configs.HEADLESS,proxy={"server": f"socks5://id:{configs.TOR_PASSWORD}@{configs.TOR_IP}:{configs.TOR_SOCKS5_PORT}"})
            context = await self.configure_browser_context(browser)
            page = await context.new_page()
            await page.set_viewport_size({"width": 300, "height": 900})
            try:
                await self.firstopen(page)
                await self.secondopen(page)
            except Exception as e:
                print(e)
            await context.close()
            await browser.close()
