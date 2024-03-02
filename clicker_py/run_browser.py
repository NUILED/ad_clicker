from playwright.sync_api import sync_playwright, TimeoutError
import random
import time
from . import config as configs
from .utility import *
from .captcha_solver import *
from playwright_recaptcha import recaptchav2


target_texts = ["Acceptă tot", "Alles accepteren", "Alle akzeptieren", "Avvis alle", "Tout accepter", "Accept all","Godkänn alla"]

def captcha_solve(page):
    try:
        with recaptchav2.SyncSolver(page) as solver:
            token = solver.solve_recaptcha(wait=True)
            print(token)
    except Exception as e:
        raise e

def is_captcha_page(page):
    return page.query_selector('.g-recaptcha') is not None


class BrowserHandler:

    def __init__(self, language, keywords, z, v):
        self.language = language
        self.keywords = keywords
        self.page = None

    def Click_ACC(self, page):
            page.wait_for_load_state('load')
            page_content = page.content()
            for target_text in target_texts:
                if target_text in page_content:
                    print("Found button with text: " + target_text)
                    button = page.locator(f'button:has-text("{target_text}")')
                    button.click()

    def try_click(self,page,target1, target):
        divs = page.query_selector_all("div[data-text-ad]")
        for div in divs:
            try:
                a = div.query_selector("a")
                href = a.get_attribute("href")
                print(href)
            except Exception as e:
                print("No link found") 
                raise e
            # You may uncomment the following lines if you want to click on the link
            # if (href == target1) or (href == target):
            try:
                a.click()
            except Exception as e:
                raise e

            page.once("load", lambda: print("page loaded!"))
            
            if is_captcha_page(page):
                try:
                    captcha_solve(page)
                except Exception as e:
                    raise e
            time.sleep(random.randint(7, 10))
            page.evaluate('window.scrollBy(0, window.innerHeight);')
    
    def firstopen(self, page):
        page.goto("http://httpbin.org/ip")
        ip_address = page.inner_text("body pre")
        time.sleep(0.5)
        print("Your IP address is:", ip_address)
        page.once("load", lambda: print("page loaded!"))
        page.goto("https://www.google.com/search?q=atm+near+me")
        page.once("load", lambda: print("page loaded!"))
        if is_captcha_page(page):
            try:
                captcha_solve(page)
            except Exception as e:
                raise e

        time.sleep(random.randint(1, 3))
        self.page = page
        page.on("load", self.Click_ACC)

    def secondopen(self, page):
        for keyword in self.keywords:
            search_url = f"https://www.google.com/search?q={keyword}"
            time.sleep(0.5)
            page.once("load", lambda: print("page loaded!"))
            if is_captcha_page(page):
                try:
                    captcha_solve(page)
                except Exception as e:
                    raise e
            time.sleep(0.5)
            time.sleep(0.5)
            page.goto(search_url)
            page.once("load", lambda: print("page loaded!"))
            try:
                self.try_click(page,configs.target , configs.target1)
            except Exception as e:
                print(e)

    def configure_browser_context(self, browser):
        context = browser.new_context(
            extra_http_headers = {"Accept-Language": configs.language},
            geolocation={
                "latitude": random.uniform(configs.casablanca_bounds["latitude_min"], configs.casablanca_bounds["latitude_max"]),
                "longitude": random.uniform(configs.casablanca_bounds["longitude_min"], configs.casablanca_bounds["longitude_max"])
            },
            permissions=["geolocation"]
        )
        user_agent = random.choice(configs.Agent)
        context.route("**/tel/*", lambda route: route.continue_())
        context.set_extra_http_headers(headers={"User-Agent": user_agent})
        return context

    def run_browser(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=configs.HEADLESS,proxy={"server": f"socks5://id:{configs.TOR_PASSWORD}@{configs.TOR_IP}:{configs.TOR_SOCKS5_PORT}"})
            context = self.configure_browser_context(browser)
            page = context.new_page()
            page.set_viewport_size({"width": 300, "height": 900})
            try:
                self.firstopen(page)
                self.secondopen(page)
            except Exception as e:
                print(e)
            context.close()
            browser.close()
