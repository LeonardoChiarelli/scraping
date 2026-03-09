import re

class ProductDetector:
    def __init__(self):
        self.price_pattern = re.compile(r"(\$|R\$|€)\s?\d+[.,]?\d*")
        self.cart_pattern = re.compile(r"(add.to.cart|comprar|adicionar.ao.carrinho)", re.I)

    def analyze(self, response):
        score = 0
        html = response.text

        if self.price_pattern.search(html):
            score += 3
        if "schema.org/Product" in html:
            score += 5
        if self.cart_pattern.search(html):
            score += 4
        if len(response.css('img::attr(src)').getall()) > 3:
            score += 1

        return score >= 8