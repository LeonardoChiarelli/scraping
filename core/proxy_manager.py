import os
import random

class ProxyManager:
    def __init__(self):
        proxy_list = os.getenv('PROXY_LIST', '')
        self.proxies = proxy_list.split(',') if proxy_list else []

    def get_random_proxy(self) -> str:
        if not self.proxies:
            return ""
        return random.choice(self.proxies)