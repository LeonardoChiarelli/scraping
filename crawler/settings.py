BOT_NAME = 'ecommerce_crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 32

DOWNLOAD_DELAY = 1.0
RANDOMIZE_DOWNLOAD_DELAY = True

DOWNLOADER_MIDDLEWARES = {
    'crawler.middlewares.RandomUserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,
}

ITEM_PIPELINES = {
    'crawler.pipelines.CleaningPipeline': 300,
    'crawler.pipelines.PostgresPipeline': 400,
}

SCHEDULER = "scrapy_rabbitmq_link.scheduler.SaaS"
RABBITMQ_CONNECTION_PARAMETERS = 'amqp://guest:guest@localhost:5672/'
RABBITMQ_QUEUE_NAME = 'scraping_queue'

DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
REDIS_URL = 'redis://localhost:6379/0'

RETRY_TIMES = 5
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429, 403]

FEEDS = {
    'exports/products_%(time)s.json': {
        'format': 'json',
        'encoding': 'utf8',
        'store_empty': False,
        'indent': 4,
    },
    'exports/products_%(time)s.csv': {
        'format': 'csv',
        'encoding': 'utf8',
        'store_empty': False,
    },
}

EXTENSIONS = {
    'crawler.extensions.ObservabilityExtension': 500,
}