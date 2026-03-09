import asyncio
import os
from core.crawler_engine import CrawlerEngine

async def main():
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    db_dsn = os.getenv("DB_DSN", "postgresql://scraper:password@localhost:5432/intelligence")
    concurrency = int(os.getenv("CONCURRENCY_LIMIT", "10"))

    engine = CrawlerEngine(redis_url, db_dsn, concurrency_limit=concurrency)
    
    engine.frontier.add_url("https://example-store.com", priority=100)
    engine.frontier.add_url("https://example-store.com/products", priority=50)

    await engine.run()

if __name__ == "__main__":
    asyncio.run(main())