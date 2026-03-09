import json
from bs4 import BeautifulSoup

def extract_product_jsonld(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    scripts = soup.find_all('script', type='application/ld+json')
    
    for script in scripts:
        if not script.string:
            continue
        try:
            data = json.loads(script.string)
            if isinstance(data, dict):
                if data.get('@type') == 'Product':
                    return _extract_fields(data)
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and item.get('@type') == 'Product':
                        return _extract_fields(item)
        except json.JSONDecodeError:
            continue
    return None

def _extract_fields(data):
    offers = data.get('offers', {})
    if isinstance(offers, list) and len(offers) > 0:
        offers = offers[0]
        
    price = offers.get('price')
    currency = offers.get('priceCurrency')
    availability = 'InStock' in offers.get('availability', '')

    brand = data.get('brand')
    if isinstance(brand, dict):
        brand = brand.get('name')

    return {
        'name': data.get('name'),
        'price': price,
        'currency': currency,
        'description': data.get('description'),
        'brand': brand,
        'sku': data.get('sku'),
        'availability': availability,
        'images': data.get('image')
    }