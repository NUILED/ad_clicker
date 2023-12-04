import random
import time
import requests
import threading
from playwright.sync_api import sync_playwright, TimeoutError
import subprocess
import datetime
import json

# for recaptcha
import urllib
import pydub
from speech_recognition import Recognizer, AudioFile
import random
import os



# def restart_docker_container(container_name_or_id, max_attempts=3, wait_seconds=2):
#     try:
#         subprocess.run(["docker", "restart", container_name_or_id], check=True)
#         print(f"Container '{container_name_or_id}' restarting...")

#         # Wait until the container is running
#         for attempt in range(max_attempts):
#             status = subprocess.check_output(["docker", "inspect", "--format='{{.State.Status}}'", container_name_or_id], text=True).strip()
            
#             if status == 'running':
#                 print(f"Container '{container_name_or_id}' is now running.")
#                 return
#             else:
#                 print(f"Waiting for container '{container_name_or_id}' to start... (Attempt {attempt + 1}/{max_attempts})")
#                 time.sleep(wait_seconds)

#         print(f"Timed out waiting for container '{container_name_or_id}' to start.")
#     except subprocess.CalledProcessError as e:
#         print(f"Error restarting container '{container_name_or_id}': {e}")

# container_name_or_id = 'your_container_name_or_id'

ip_address = "169.197.83.75"
port = "6332"
class SolveCaptcha:
    def __init__(self, page):
        self.page = page
        self.main_frame = None
        self.recaptcha = None

    def delay(self):
        self.page.wait_for_timeout(random.randint(1, 3) * 1000)

    def presetup(self):
        name = self.page.locator(
            "//iframe[@title='reCAPTCHA']").get_attribute("name")
        self.recaptcha = self.page.frame(name=name)

        self.recaptcha.click("//div[@class='recaptcha-checkbox-border']")
        self.delay()
        s = self.recaptcha.locator("//span[@id='recaptcha-anchor']")
        if s.get_attribute("aria-checked") != "false":  # solved already
            return

        self.main_frame = self.page.frame(name=self.page.locator(
            "//iframe[contains(@src,'https://www.google.com/recaptcha/api2/bframe?')]").get_attribute("name"))
        self.main_frame.click("id=recaptcha-audio-button")

    def start(self):
        self.presetup()
        tries = 0
        while (tries <= 5):
            self.delay()
            try:
                self.solve_captcha()
            except Exception as e:
                print(e)
                self.main_frame.click("id=recaptcha-reload-button")
                exit
            else:
                s = self.recaptcha.locator("//span[@id='recaptcha-anchor']")
                if s.get_attribute("aria-checked") != "false":
                    self.page.click("id=recaptcha-demo-submit")
                    self.delay()
                    break
            tries += 1

    def solve_captcha(self):
        self.main_frame.click(
            "//button[@aria-labelledby='audio-instructions rc-response-label']")
        href = self.main_frame.locator(
            "//a[@class='rc-audiochallenge-tdownload-link']").get_attribute("href")

        urllib.request.urlretrieve(href, "audio.mp3")

        sound = pydub.AudioSegment.from_mp3(
            "audio.mp3").export("audio.wav", format="wav")

        recognizer = Recognizer()

        recaptcha_audio = AudioFile("audio.wav")
        with recaptcha_audio as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)
        print(text)
        self.main_frame.fill("id=audio-response", text)
        self.main_frame.click("id=recaptcha-verify-button")
        self.delay()

    def __del__(self):
        os.remove("audio.mp3")
        os.remove("audio.wav")

def is_captcha_page(page):

    # Check if the reCAPTCHA widget is present
    return page.query_selector('.g-recaptcha') is not None


class BrowserHandler:
    def __init__(self, ip_address, port, language, keywords, z, v):
        self.ip_address = ip_address
        self.port = port
        self.page = None
        self.language = language
        self.keywords = keywords
        self.z = z
        self.v = v
    def firstopen(self):
        self.page.goto("https://www.whoer.net/")
        self.page.wait_for_load_state("load")
        self.page.goto("https://www.google.com/search?q=atm+near+me")
        self.page.wait_for_load_state("load")
        page_content = self.page.content()
        if is_captcha_page(self.page):
            captcha_solver = SolveCaptcha(self.page)
            captcha_solver.start()
            del captcha_solver
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
            time.sleep(random.randint(3, 6))
            search_url = f"https://www.google.com/search?q={keyword}"
            self.page.wait_for_load_state("load")
            if is_captcha_page(self.page):
                captcha_solver = SolveCaptcha(self.page)
                captcha_solver.start()
                del captcha_solver
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
                    except:
                        print("No Clickable Link Found")
                    self.page.wait_for_load_state("load")
                if is_captcha_page(self.page):
                    captcha_solver = SolveCaptcha(self.page)
                    captcha_solver.start()
                    del captcha_solver
                time.sleep(random.randint(8, 20))
                self.page.evaluate('window.scrollBy(0, window.innerHeight);')


    def configure_browser_context(self, browser, proxy_info):
        context = browser.new_context(
        extra_http_headers = {"Accept-Language": language},
        proxy = proxy_info,
        geolocation={
            "latitude": random.uniform(casablanca_bounds["latitude_min"], casablanca_bounds["latitude_max"]),
            "longitude": random.uniform(casablanca_bounds["longitude_min"], casablanca_bounds["longitude_max"])
        },
        permissions=["geolocation"]
    )
        user_agent = random.choice([
    # iOS devices
                "Mozilla/5.0 (Linux; Android 11; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.185 Mobile Safari/537.36"
"Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36",
   "Mozilla/5.0 (Linux; Android 11; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36",
   "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36",

    # iPad User Agents
   "Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
   "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
   "Mozilla/5.0 (iPad; CPU OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Mobile/15E148 Safari/604.1"
              "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X; en-us) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
           "Mozilla/5.0 (Linux; Android 12; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.9999.99 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X; en-us) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
         ]
)
        context.route("**/tel/*", lambda route: route.continue_())
        context.set_extra_http_headers(headers={"User-Agent": user_agent})
        return context

    def run_browser(self):
        time.sleep(random.randint(2, 6))
        i = 1
        with sync_playwright() as p:
            proxy_info = {"server": f"http://{self.ip_address}:{self.port}",
            "username": "q9j6y",
            "password": "r9b792nu"
            }  
            browser = p.firefox.launch(headless=True)
            context = self.configure_browser_context(browser,proxy_info)
            page = context.new_page()
            page.set_viewport_size({"width": 300, "height": 630})
            self.page = page
            try:
                if i == 1:
                    self.firstopen()
                    i = 2
                if is_captcha_page(page):
                    captcha_solver = SolveCaptcha(self.page)
                    captcha_solver.start()
                    del captcha_solver
                self.secondopen()
            except TimeoutError:
                print("TimeoutError")
            context.close()
            browser.close()
if __name__ == "__main__":
    language = "fr-MA"
    keywords = ["medecin a domicile casablanca","medecin de nuit casablanca","sos medecin casablanca","docteur a domicile casablanca"]
    az = "https://www.sosmedecinsmaroc.com/urgences"

    v = "https://sos-medecin.ma/"
    b = "https://docteurcasablanca.ma/"
    t = "https://medecin-a-domicile.ma/"
    z = "https://www.urgence-casablanca.ma/"

    casablanca_bounds = {
        "latitude_min": 33.5174,
        "latitude_max": 33.6362,
        "longitude_min": -7.6875,
        "longitude_max": -7.5042
    }

    num_threads = 10
    threads = []
    def run_thread():
        handler = BrowserHandler(ip_address, port, language, keywords, v, z)
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
