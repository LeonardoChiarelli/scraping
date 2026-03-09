import re

class CleaningPipeline:
    def __init__(self):
        self.currency_pattern = re.compile(r"[^\d.,]")

    def process(self, item):
        if not item or "price" not in item:
            return item

        raw_price = item["price"]
        clean_price = self.currency_pattern.sub("", raw_price)
        clean_price = clean_price.replace(",", ".")

        try:
            item["price_numeric"] = float(clean_price)
        except ValueError:
            item["price_numeric"] = None

        return item