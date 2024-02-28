from logging import Logger as logger
from clicker_py.config import *
from clicker_py.proxy import TorProxy
from clicker_py.run_browser import BrowserHandler
from clicker_py.utility import check_tor_running
from clicker_py.utility import *
import asyncio
import time

if check_tor_running(TOR_IP, TOR_SOCKS5_PORT):
        logger.info('Tor is running. Connecting to Tor...')
        logger.info('Connected to Tor.')

proxy_manager = TorProxy(TOR_IP, TOR_PORT, TOR_PASSWORD, TOR_CONTROL_PORT, TOR_DELAY)

async def main():
    retries = 0
    proxy = proxy_manager.get_next()
    proxy.auth
    time.sleep(2)
    while True:
        retries += 1
        if retries % 2 == 0:
            proxy = proxy_manager.get_next()
            proxy.auth
            time.sleep(1.2)
            print('Failed 2 times in a row. Using next proxy')
        try:
            handler =  BrowserHandler(language, keywords, target1, target2)
            await handler.run_browser()
        except Exception as e:
            print("",e)

if __name__ == "__main__":
    asyncio.run(main())