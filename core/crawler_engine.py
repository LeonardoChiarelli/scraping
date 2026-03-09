import asyncio
import hashlib
from curl_cffi.requests import AsyncSession
from core.scheduler import DistributedFrontier
from storage.postgres_repository import PostgresRepository
from parsers.product_detector import ProductDetector
from parsers.jsonld_parser import JSONLDParser
from parsers.html_product_parser import HTMLProductParser
from pipelines.cleaning_pipeline import CleaningPipeline

class CrawlerEngine:
    def __init__(self, redis_url, db_dsn, concurrency_limit=50):
        self.frontier = DistributedFrontier(redis_url)
        self.db = PostgresRepository(db_dsn)
        self.concurrency_limit = concurrency_limit
        self.session = None
        self.detector = ProductDetector()
        self.jsonld_parser = JSONLDParser()
        self.html_parser = HTMLProductParser()
        self.cleaner = CleaningPipeline()

    async def initialize(self):
        await self.db.connect()
        self.session = AsyncSession(impersonate="chrome116")

    async def run(self):
        await self.initialize()
        workers = [asyncio.create_task(self._worker()) for _ in range(self.concurrency_limit)]
        await asyncio.gather(*workers)

    async def _worker(self):
        while True:
            url = self.frontier.get_next_url()
            
            if not url:
                await asyncio.sleep(2)
                continue

            html_content = await self._fetch(url)
            
            if html_content and self.detector.analyze(html_content):
                await self._process_and_store(url, html_content)

    async def _fetch(self, url):
        try:
            response = await self.session.get(url, timeout=15)
            if response.status_code in (403, 429, 503):
                self.frontier.add_url(url, priority=10)
                return None
            response.raise_for_status()
            return response.text
        except Exception:
            return None

    async def _process_and_store(self, url, html_content):
        parsed_data = self.jsonld_parser.parse(html_content, url)
        
        if not parsed_data or not parsed_data.get("price"):
            parsed_data = self.html_parser.parse(html_content, url)

        if parsed_data and parsed_data.get("name"):
            cleaned_data = self.cleaner.process(parsed_data)
            cleaned_data["fingerprint"] = hashlib.sha256(f"{url}_{cleaned_data['name']}".encode()).hexdigest()
            await self.db.insert_product(cleaned_data)