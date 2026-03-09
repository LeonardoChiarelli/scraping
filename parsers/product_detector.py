import re

price_pattern = r"(\$|R\$|€)\s?\d+[.,]?\d*"


def is_product_page(html):

    score = 0

    if re.search(price_pattern, html):
        score += 3

    if "schema.org/Product" in html:
        score += 5

    if "add-to-cart" in html:
        score += 3

    if score >= 6:
        return True

    return False