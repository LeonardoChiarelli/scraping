import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from detectors.product_detector import ProductDetector
from detectors.api_detector import APIDetector
from parsers.jsonld_parser import extract_product_jsonld
from parsers.html_parser import parse_html

class EcommerceSpider(CrawlSpider):
    name = 'ecommerce_spider'
    
    rules = (
        Rule(LinkExtractor(deny=(r'/cart', r'/checkout', r'/login')), callback='parse_page', follow=True),
    )

    def __init__(self, *args, **kwargs):
        super(EcommerceSpider, self).__init__(*args, **kwargs)
        self.product_detector = ProductDetector()
        self.api_detector = APIDetector()

    def parse_page(self, response):
        if not hasattr(response, 'text'):
            return

        endpoints = self.api_detector.extract_endpoints(response.text)
        for endpoint in endpoints:
            if endpoint.startswith('/'):
                yield response.follow(endpoint, callback=self.parse_api_response)

        if self.product_detector.analyze(response):
            data = extract_product_jsonld(response.text)
            if not data:
                data = parse_html(response)
            
            if data and data.get('name'):
                data['url'] = response.url
                yield data

    def parse_api_response(self, response):
        pass