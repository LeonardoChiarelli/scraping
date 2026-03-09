def parse_html(response):
    name = response.css('h1::text').get()
    price = response.css('[itemprop="price"]::text, .price::text, .product-price::text').get()
    description = response.css('[itemprop="description"]::text, .description::text').get()
    brand = response.css('[itemprop="brand"]::text, .brand::text').get()
    sku = response.css('[itemprop="sku"]::text').get()
    images = response.css('img::attr(src)').getall()

    if not name or not price:
        return None

    return {
        'name': name.strip() if name else None,
        'price': price.strip() if price else None,
        'description': description.strip() if description else None,
        'brand': brand.strip() if brand else None,
        'sku': sku.strip() if sku else None,
        'images': images
    }