from scrapy.spiders import SitemapSpider
from detectors.product_detector import ProductDetector
from parsers.jsonld_parser import extract_product_jsonld
from parsers.html_parser import parse_html

class EcommerceSitemapSpider(SitemapSpider):
    name = 'sitemap_spider'
    sitemap_urls = ['https://example.com/robots.txt']
    sitemap_rules = [
        ('/produto/', 'parse_product'),
        ('/p/', 'parse_product'),
    ]

    def __init__(self, *args, **kwargs):
        super(EcommerceSitemapSpider, self).__init__(*args, **kwargs)
        self.product_detector = ProductDetector()

    def parse_product(self, response):
        if self.product_detector.analyze(response):
            data = extract_product_jsonld(response.text)
            if not data:
                data = parse_html(response)
            
            if data and data.get('name'):
                data['url'] = response.url
                yield data