from crawler.queue import push_url


seed_urls = [
    "https://example-store.com"
]


def seed():

    for url in seed_urls:
        push_url(url)