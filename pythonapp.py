import random
import time
import threading
from playwright.sync_api import sync_playwright, TimeoutError,Page, Playwright
#from playwright.sync_api import devices
import typing


# for recaptcha

import os
from recaptcha_challenger import new_audio_solver

def is_captcha_page(page):
    # Check if the reCAPTCHA widget is present
    return page.query_selector('.g-recaptcha') is not None

# class motion:
#     def __init__(self, page):
#         self.page = page
#     def run(self):
#         self.motio()
    


def motion(page) -> typing.Optional[str]:
    solver = new_audio_solver()
    if solver.utils.face_the_checkbox(page):
        solver.anti_recaptcha(page)
    return solver.response
class BrowserHandler:
    def __init__(self, language, keywords, z, v):
        self.page = None
        self.language = language
        self.keywords = keywords
        self.z = z
        self.v = v

    def firstopen(self):
        self.page.goto("https://www.google.com/search?q=atm+near+me")
        time.sleep(random.randint(3, 6))
        if is_captcha_page(self.page):
            self.motion (self.page)
        page_content = self.page.content()
        target_texts = ["Acceptă tot", "Alles accepteren", "Alle akzeptieren", "Tout accepter", "Accept all","Godkänn alla"]
        for target_text in target_texts:
            if target_text in page_content:
                print("Found button with text: " + target_text)
                button =self.page.locator(f'button:has-text("{target_text}")')
                button.click()
        self.page.reload()
        time.sleep(random.randint(3, 6))


    def secondopen(self):
        for keyword in self.keywords:
            search_url = f"https://www.google.com/search?q={keyword}"
            time.sleep(random.randint(3, 6))
            if is_captcha_page(self.page):
                print("captchaoas")
                self.motion(self.page)
            self.page.goto(search_url)
            self.page.reload()
            time.sleep(random.randint(3, 8))
            divs = self.page.query_selector_all("div[data-text-ad]")
            for div in divs:
                try:
                    a = div.query_selector("a")
                    href = a.get_attribute("href")
                    if a and href == self.z or href == self.v:
                        a.click()
                        print(href)
                        self.page.evaluate('window.scrollBy(0, window.innerHeight);')
                        time.sleep(random.randint(6, 10))
                except:
                    print("HELP")
                    continue
                # if a: #and href == self.z or self.v == href:  # Corrected the condition
                #     self.page.evaluate('window.scrollBy(0, window.innerHeight);')
                    # except:
                    #     self.page.evaluate('window.scrollBy(0, window.innerHeight);')
                # if is_captcha_page(self.page):
                #     self.self.motion = self.page
                #     self.motion.run()
        return

    def configure_browser_context(self, browser,p):
        smartphones = [device for device in p.devices.keys()]
        device = random.choice(smartphones)
        print(device)
        context = browser.new_context(
        #**p.devices[device],
        extra_http_headers = {"Accept-Language": language},
        geolocation={
            "latitude": random.uniform(casablanca_bounds["latitude_min"], casablanca_bounds["latitude_max"]),
            "longitude": random.uniform(casablanca_bounds["longitude_min"], casablanca_bounds["longitude_max"])
        },
        permissions=["geolocation"]
        )
        context.route("**/tel/*", lambda route: route.continue_())
        return context

    def run_browser(self):
        time.sleep(random.randint(2, 6))
        i = 1
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = self.configure_browser_context(browser,p)
            page = context.new_page()
            page.set_viewport_size({"width": 300, "height": 736})
            self.page = page
            try:
                if i == 1:
                    self.firstopen()
                    i = 2
                if is_captcha_page(self.page):
                    self.motion (self.page)
                    #cap.run()
                self.secondopen()
            except TimeoutError:
                print("TimeoutError")
            context.close()
            browser.close()
if __name__ == "__main__":
    language = "fr-MA"
    keywords = ["medecin a domicile casablanca","medecin de nuit casablanca","sos medecin casablanca","service aide à la personne"]
    az = "https://www.sosmedecinsmaroc.com/urgences"

    v = "https://sos-medecin.ma/"
    b = "https://docteurcasablanca.ma/"
    z = "https://www.docteurcasablanca.ma/"
    t = "https://medecin-a-domicile.ma/"
    #z = "https://www.google.com/search?q=atm+near+me"

    casablanca_bounds = {
        "latitude_min": 33.5174,
        "latitude_max": 33.6362,
        "longitude_min": -7.6875,
        "longitude_max": -7.5042
    }

    num_threads = 1
    threads = []
    def run_thread():
        handler = BrowserHandler(language, keywords, b,z)
        handler.run_browser()
    while True:
        # restart_docker_container(container_name_or_id)        
        for _ in range(num_threads):
            thread = threading.Thread(target=run_thread)
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        threads = []  # Clear the threads list after joining
