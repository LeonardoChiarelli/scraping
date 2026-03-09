import json
from bs4 import BeautifulSoup


def extract_product_jsonld(html):

    soup = BeautifulSoup(html, "lxml")

    scripts = soup.find_all(
        "script",
        type="application/ld+json"
    )

    for script in scripts:

        try:

            data = json.loads(script.string)

            if data.get("@type") == "Product":

                return data

        except:
            pass

    return None