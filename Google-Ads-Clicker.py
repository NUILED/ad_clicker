import random
import time
import threading
from playwright.sync_api import sync_playwright
import random
import time
import threading
from playwright.sync_api import sync_playwright

def read_proxies(file_path):
    with open(file_path, 'r') as file:
        proxies = file.read().splitlines()
    return proxies

def run_browser(proxy_list):
    while True:
        proxy = random.choice(proxy_list)
        proxy_parts = proxy.split(':')
        proxy_address = proxy_parts[0]
        proxy_port = int(proxy_parts[1])

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, proxy=f"http://{proxy_address}:{proxy_port}")
            context = browser.new_context(
                geolocation={
                    "latitude": random.uniform(casablanca_bounds["latitude_min"], casablanca_bounds["latitude_max"]),
                    "longitude": random.uniform(casablanca_bounds["longitude_min"], casablanca_bounds["longitude_max"])
                },
                permissions=["geolocation"]
            )
            user_agent = random.choice([
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
           # "Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; Lumia 950) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36 Edge/40.15063.0.0"
               ])

            context.set_extra_http_headers(headers={"User-Agent": user_agent})
            page = context.new_page()
            i = 1
            for keyword in keywords:
                try:
                    if i == 1:
                        viewport_width = 300
                        viewport_height = 1200
                        page.set_viewport_size({"width": viewport_width, "height": viewport_height})
                        page.goto("https://www.google.com/search?q=atm+near+me")
                        button_locator = page.locator('button:has-text("tout accepter")')
                        button_locator.click()
                        i = 2
                        time.sleep(random.randint(2, 6))
                        page.reload()
                        time.sleep(random.randint(2, 4))
                    search_url = f"https://www.google.com/search?q={keyword}"
                    page.goto(search_url)
                    time.sleep(random.randint(3, 8))
                    # page.reload()
                    divs = page.query_selector_all("div[data-text-ad]")
                    for div in divs:
                        a = div.query_selector("a")
                        if a:
                            href = a.get_attribute("href")
                            a.click()
                            print(page.url)
                            time.sleep(random.randint(8, 20))
                            page.evaluate('window.scrollBy(0, window.innerHeight);')
                            break
                        else:
                            print("not clicked")
                except:
                    print("PROBLEMM")
                    continue
            context.close()
            browser.close()

if __name__ == "__main__":
    proxy_file_path = "proxy.txt"
    proxy_list = read_proxies(proxy_file_path)

    keywords = ["medecin a domicile", "sos medecin casablanca", "docteur a domicile"]
    casablanca_bounds = {
        "latitude_min": 33.5174,
        "latitude_max": 33.6362,
        "longitude_min": -7.6875,
        "longitude_max": -7.5042
    }

    num_threads = 4
    threads = []

    while True:
        for _ in range(num_threads):
            thread = threading.Thread(target=run_browser, args=(proxy_list,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        threads = [] 
