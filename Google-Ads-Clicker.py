from logging import Logger as logger
from clicker_py.config import *
from clicker_py.proxy import TorProxy
from clicker_py.run_browser import BrowserHandler
from clicker_py.utility import check_tor_running
from clicker_py.utility import *


if check_tor_running(TOR_IP, TOR_SOCKS5_PORT):
        logger.info('Tor is running. Connecting to Tor...')
        logger.info('Connected to Tor.')

proxy_manager = TorProxy(TOR_IP, TOR_PORT, TOR_PASSWORD, TOR_CONTROL_PORT, TOR_DELAY)

def main():
    retries = 0
    proxy = proxy_manager.get_next()
    proxy.auth
    while True:
        retries += 1
        if retries % 2 == 0:
            proxy = proxy_manager.get_next()
            proxy.auth
            print('Failed 2 times in a row. Using next proxy')
        try:
            handler =  BrowserHandler(language, keywords, target1, target2)
            handler.run_browser()
            del handler
        except Exception as e:
            print("",e)

if __name__ == "__main__":
    main()