import time
from abc import ABC, abstractmethod
from typing import Optional

from stem import Signal
from stem.control import Controller
from requests.auth import AuthBase
from .utility import Proxy

class ProxyManager(ABC):
    """
    Abstract class for proxy managers

    Proxy manager needed to switch proxies after each account creation
    """

    @abstractmethod
    def get_next(self) -> Optional[Proxy]:
        """
        Get next proxy
        """
        ...


class TorProxy(ProxyManager):
    """Proxy manager based on Tor"""

    def __init__(self, ip: str, port: int, password: str, control_port: int, delay: int = 5):
        self.ip = ip
        self.port = port
        self.password = password
        self.control_port = control_port
        self.delay = delay
        self.circuit_id = None

        self.controller = Controller.from_port(port=self.control_port)
        self.controller.authenticate(self.password)
    
    def establish_exit_node_circuit(self):
        try:
            # Get a list of available exit nodes
            exit_nodes = [desc.fingerprint for desc in self.controller.get_network_statuses() if 'Exit' in desc.flags] # we try to reduce nodes bettwing my request and exit node to make more speed and prevent loading error 
            if exit_nodes:
                # Configure a circuit using the exit node as the only hop
                circuit_id = self.controller.new_circuit(path=[exit_nodes[0]], await_build=True)
                self.circuit_id = circuit_id
            else:
                print("No exit nodes available.")
        except Exception as e:
            print("Error establishing circuit:", e)
            return None
    
    @property
    def proxy(self) -> Proxy:
        return Proxy(self.ip, self.port)

    def get_next(self):
        time.sleep(self.delay)  # Delay for safety
        self.controller.signal(Signal.NEWNYM)
        self.establish_exit_node_circuit()
        return self.proxy

    def __str__(self) -> str:
        return f'{self.ip}:{self.port}'

class EmptyProxy(ProxyManager):
    """In case if we want to use local IP address"""
    def get_next(self):
        return None

    def __str__(self) -> str:
        return 'No proxy'