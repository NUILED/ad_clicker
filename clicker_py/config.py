"""Configurations"""
args = [
            '--deny-permission-prompts',
            '--no-default-browser-check',
            '--no-first-run',
            '--ignore-certificate-errors',
            '--no-service-autorun',
            '--password-store=basic',
            '--window-size=640,480',
        ]
Agent = [                "Mozilla/5.0 (Linux; Android 11; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.185 Mobile Safari/537.36",
"Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36",
   "Mozilla/5.0 (Linux; Android 11; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36",
   "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36",

    # iPad User Agents
   "Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
   "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
   "Mozilla/5.0 (iPad; CPU OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Mobile/15E148 Safari/604.1"
              "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X; en-us) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
           "Mozilla/5.0 (Linux; Android 12; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.9999.99 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X; en-us) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"]
language = "fr-MA"
keywords = ["medecin a domicile casablanca","medecin de nuit casablanca","sos medecin casablanca","docteur a domicile casablanca"]
owners = "https://www.sosmedecinsmaroc.com/urgences"

target = "https://medecin-a-domicile.ma/"
target1 = "https://sos-medecin.ma/"
target2 = "https://docteurcasablanca.ma/"
target3= "https://www.urgence-casablanca.ma/"


casablanca_bounds = {
        "latitude_min": 33.5174,
        "latitude_max": 33.6362,
        "longitude_min": -7.6875,
        "longitude_max": -7.5042
    }
# Tor proxy config
TOR_IP = '127.0.0.1'
TOR_PORT = 1881
TOR_SOCKS5_PORT = 9050
TOR_CONTROL_PORT = 9051
TOR_PASSWORD = 'Passwort'
TOR_DELAY = 5
HEADLESS = True
