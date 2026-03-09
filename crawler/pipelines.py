import re
from scrapy.exceptions import DropItem
from storage.postgres import PostgresRepository

class CleaningPipeline:
    def process_item(self, item, spider):
        if not item.get('name') or not item.get('price'):
            raise DropItem("Produto inválido ou incompleto")
            
        price_str = str(item['price'])
        price_clean = re.sub(r'[^\d.,]', '', price_str).replace(',', '.')
        
        try:
            item['price'] = float(price_clean)
        except ValueError:
            item['price'] = 0.0
            
        return item

class PostgresPipeline:
    def __init__(self, db_dsn: str):
        self.repo = PostgresRepository(db_dsn)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_dsn=crawler.settings.get('DB_DSN')
        )

    def open_spider(self, spider):
        self.repo.connect()

    def close_spider(self, spider):
        self.repo.disconnect()

    def process_item(self, item, spider):
        self.repo.upsert_product(item)
        return item