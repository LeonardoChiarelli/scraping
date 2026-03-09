from bs4 import BeautifulSoup

class HTMLProductParser:
    def parse(self, html, url):
        soup = BeautifulSoup(html, "lxml")
        
        name_elem = soup.find("h1")
        price_elem = soup.select_one(".price, [data-price], [itemprop='price']")
        desc_elem = soup.select_one(".description, [itemprop='description']")
        
        if not name_elem or not price_elem:
            return None

        return {
            "url": url,
            "name": name_elem.get_text(strip=True),
            "price": price_elem.get_text(strip=True),
            "description": desc_elem.get_text(strip=True) if desc_elem else None
        }