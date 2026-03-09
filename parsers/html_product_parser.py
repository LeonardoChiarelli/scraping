from bs4 import BeautifulSoup


def parse_product_html(html):

    soup = BeautifulSoup(html, "lxml")

    name = soup.find("h1")

    price = soup.select_one(".price")

    description = soup.select_one(".description")

    return {

        "name": name.text if name else None,
        "price": price.text if price else None,
        "description": description.text if description else None

    }