import random
from core.proxy_manager import ProxyManager

class RandomUserAgentMiddleware:
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.user_agents))

class ProxyMiddleware:
    def __init__(self):
        self.proxy_manager = ProxyManager()

    def process_request(self, request, spider):
        proxy = self.proxy_manager.get_random_proxy()
        if proxy:
            request.meta['proxy'] = proxy