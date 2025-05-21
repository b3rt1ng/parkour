import requests

class PageCache:
    def __init__(self):
        self.cache = {}

    def fetch(self, url):
        if url in self.cache:
            return self.cache[url]
        try:
            response = requests.get(url, timeout=0.8)
            result = (response.status_code, response.text, response.elapsed.total_seconds(), len(response.content))
        except requests.RequestException:
            result = (None, None, None, None)
        self.cache[url] = result
        return result
