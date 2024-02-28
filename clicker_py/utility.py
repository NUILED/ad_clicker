from typing import Optional, Dict, Tuple
from dataclasses import dataclass
from . import exceptions

import requests

@dataclass
class  Proxy:
    """
    Proxy dataclass
    """
    host: str
    port: int
    scheme: str = 'http'
    user: Optional[str] = None
    password: Optional[str] = None

    def to_dict(self) -> Dict[str, str]:
        """
        Convert proxy to dict for requests library
        """
        return {
            'http': str(self),
            'https': str(self),
        }

    def to_string(self) -> str:
        """
        Get proxy string representation
        """
        if self.password is None:
            return f'{self.scheme}://{self.host}:{self.port}'
        return f'{self.scheme}://{self.user}:{self.password}@{self.host}:{self.port}'

    @property
    def auth(self) -> Optional[Tuple[str, str]]:
        """
        Get proxy auth tuple
        """
        if self.user is None or self.password is None:
            return None
        return self.user, self.password

    @classmethod
    def from_str(cls, proxy: str) -> 'Proxy':
        """
        Create proxy from string. Alias for :func:`parse_proxy`

        :param proxy: Proxy string
        :return: Proxy object
        """
        return parse_proxy(proxy)

    def __str__(self) -> str:
        return self.to_string()


def generate_username() -> str:
    username = _generate_username(1)[0] + str(random.randint(100, 1000))
    return username


def generate_password(length: int = 12) -> str:
    characters = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password


def load_proxies(path: str) -> list[str]:
    """
    Load proxies from file

    File format:
    IP:PORT without protocol
    """

    if not os.path.exists(path):
        return []

    proxies = []

    with open(path, 'r', encoding='utf-8') as f:
        for _, line in enumerate(f):
            line = line.strip()
            if line == '' or line.startswith('#'):
                continue
            proxies.append(line)

    return proxies


def check_tor_running(ip: str, port: int) -> bool:
    try:
        r = requests.get('https://check.torproject.org/api/ip', proxies={'https': f'socks5://{ip}:{port}'}, timeout=5)
        return r.json()['IsTor'] is True
    except Exception:
        return False

def setup_proxy(proxy: Proxy) -> str:
    if proxy.auth is None:
        return proxy.to_string()
