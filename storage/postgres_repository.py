import asyncpg
import json

class PostgresRepository:
    def __init__(self, dsn):
        self.dsn = dsn
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(self.dsn)

    async def insert_product_batch(self, products):
        query = """
        INSERT INTO products (fingerprint, url, data)
        VALUES ($1, $2, $3)
        ON CONFLICT (fingerprint) DO UPDATE
        SET data = EXCLUDED.data
        """
        records = [
            (p['fingerprint'], p['url'], json.dumps(p)) for p in products
        ]
        
        async with self.pool.acquire() as conn:
            await conn.executemany(query, records)