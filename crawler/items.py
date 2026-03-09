import scrapy

class ProductItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    description = scrapy.Field()
    brand = scrapy.Field()
    sku = scrapy.Field()
    availability = scrapy.Field()
    images = scrapy.Field()
    url = scrapy.Field()