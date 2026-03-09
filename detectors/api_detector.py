import re

class APIDetector:
    def __init__(self):
        self.api_patterns = [
            re.compile(r"['\"](/api/v\d+/.*?)['\"]", re.I),
            re.compile(r"['\"](/graphql.*?)['\"]", re.I),
            re.compile(r"fetch\(['\"](.*?)['\"]", re.I),
            re.compile(r"axios\.get\(['\"](.*?)['\"]", re.I)
        ]

    def extract_endpoints(self, html):
        endpoints = set()
        for pattern in self.api_patterns:
            matches = pattern.findall(html)
            for match in matches:
                endpoints.add(match)
        return list(endpoints)