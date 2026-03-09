import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def start_worker():
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'crawler.settings')
    settings = get_project_settings()
    
    process = CrawlerProcess(settings)
    
    spider_type = os.getenv('SPIDER_TYPE', 'ecommerce_spider')
    process.crawl(spider_type)
    process.start()

if __name__ == '__main__':
    start_worker()