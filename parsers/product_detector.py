import re

class ProductDetector:
    def __init__(self):
        self.price_pattern = re.compile(r"(\$|R\$|€)\s?\d+[.,]?\d*")

    def analyze(self, html):
        score = 0
        
        if self.price_pattern.search(html):
            score += 3
        if "schema.org/Product" in html:
            score += 5
        if "add-to-cart" in html.lower():
            score += 3

        return score >= 6