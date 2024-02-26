from playwright_recaptcha import recaptchav2
from playwright.sync_api import sync_playwright, TimeoutError
import random
from .exceptions import Captcha_not_solved
from .utility import setup_proxy 
import time
from . import config as configs

def captcha_solve(page):
    with recaptchav2.AsyncSolver(page) as solver:
        token = solver.solve_recaptcha(wait=True)
        if token:
            print("solved")
        else:
            raise Captcha_not_solved
def is_captcha_page(page):

    # Check if the reCAPTCHA widget is present
    return page.query_selector('.g-recaptcha') is not None

class BrowserHandler:
    def __init__(self, proxy, language, keywords, z, v):
        self.proxy = proxy
        self.page = None
        self.language = language
        self.keywords = keywords
        self.z = z
        self.v = v

    def firstopen(self):
        self.page.goto("https://www.google.com/search?q=atm+near+me")
        self.page.wait_for_load_state("load")
        page_content = self.page.content()
        if is_captcha_page(self.page):
            captcha_solve(self.page)
        target_texts = ["Acceptă tot", "Alles accepteren", "Alle akzeptieren", "Tout accepter", "Accept all","Godkänn alla"]
        for target_text in target_texts:
            if target_text in page_content:
                print("Found button with text: " + target_text)
                button =self.page.locator(f'button:has-text("{target_text}")')
                button.click()
        time.sleep(random.randint(3, 6))
        self.page.reload()

    def secondopen(self):
        for keyword in self.keywords:
            search_url = f"https://www.google.com/search?q={keyword}"
            time.sleep(random.randint(3, 6))
            self.page.wait_for_load_state("load")
            if is_captcha_page(self.page):
                    captcha_solve(self.page)
            self.page.goto(search_url)
            self.page.wait_for_load_state("load")
            time.sleep(random.randint(3, 8))
            divs = self.page.query_selector_all("div[data-text-ad]")
            for div in divs:
                try:
                    a = div.query_selector("a")
                    href = a.get_attribute("href")
                except:
                    print("No link found")
                if (href == self.z ) or (href == self.v):  # Corrected the condition
                    print(href)
                    try:
                        a.click()
                    except Exception as e:
                        print(e)
                    self.page.wait_for_load_state("load")
                if is_captcha_page(self.page):
                    captcha_solve(self.page)
                time.sleep(random.randint(8, 20))
                self.page.evaluate('window.scrollBy(0, window.innerHeight);')

    def configure_browser_context(self, browser):
        context = browser.new_context(
        extra_http_headers = {"Accept-Language": configs.language},
        proxy = setup_proxy(self.proxy),
        geolocation={
            "latitude": random.uniform(configs.casablanca_bounds["latitude_min"], configs.casablanca_bounds["latitude_max"]),
            "longitude": random.uniform(configs.casablanca_bounds["longitude_min"], configs.casablanca_bounds["longitude_max"])
        },
        
        permissions=["geolocation"]
    )
        user_agent = random.choice(configs.Agent)
        context.route("**/tel/*", lambda route: route.continue_())
        context.set_extra_http_headers(headers={"User-Agent": user_agent}) #we will try to use playwright devices to make us memaking mobile phones
        return context

    def run_browser(self):
        time.sleep(random.randint(2, 6))
        i = 1
        with sync_playwright() as p:

            browser = p.firefox.launch(headless=configs.HEADLESS)
            context = self.configure_browser_context(browser)
            page = context.new_page()
            self.page = page
            try:
                if i == 1:  #if you want to run it multiple time;
                    self.firstopen()
                    i = 2
                if is_captcha_page(page):
                    captcha_solve(self.page)
                self.secondopen()
            except TimeoutError:
                print("TimeoutError")
            context.close()
            browser.close()