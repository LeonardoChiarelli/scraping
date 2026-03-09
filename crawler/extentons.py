import logging
from scrapy import signals

class ObservabilityExtension:
    def __init__(self, stats):
        self.stats = stats
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler.stats)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        return ext

    def spider_closed(self, spider, reason):
        pages_crawled = self.stats.get_value('response_received_count', 0)
        items_scraped = self.stats.get_value('item_scraped_count', 0)
        errors = self.stats.get_value('log_count/ERROR', 0)
        start_time = self.stats.get_value('start_time')
        finish_time = self.stats.get_value('finish_time')

        if start_time and finish_time:
            duration = (finish_time - start_time).total_seconds()
            pages_per_minute = (pages_crawled / duration) * 60 if duration > 0 else 0
        else:
            pages_per_minute = 0

        self.logger.info("=== RELATÓRIO DE OBSERVABILIDADE ===")
        self.logger.info(f"Páginas rastreadas: {pages_crawled}")
        self.logger.info(f"Taxa (Páginas/minuto): {pages_per_minute:.2f}")
        self.logger.info(f"Produtos extraídos: {items_scraped}")
        self.logger.info(f"Erros encontrados: {errors}")
        self.logger.info("====================================")