import requests
from bs4 import BeautifulSoup
from .http_cache import PageCache
from urllib.parse import urljoin, urlparse

cache = PageCache()

class page_mapper:
    def __init__(self, url=None):
        self.url = url
        self.content = self.get_page(url) if url else None
        self.response_time = None

    def get_page(self, url):
        try:
            code, text, time, size = cache.fetch(url)
            if code == 200:
                self.response_time = time
                return text
            else:
                print(f"Error: {code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
        
    def get_links(self):
        if self.content:
            soup = BeautifulSoup(self.content, 'html.parser')
            links = [a.get('href') for a in soup.find_all('a', href=True)]
            links = [link for link in links if link and '#' not in link]
            # images
            links += [img.get('src') for img in soup.find_all('img', src=True)]
            # RSS feeds
            links += [link.get('src') for link in soup.find_all('script', src=True)]
            return links
        else:
            print("No content to parse.")
            return []
    
    def is_directory_listing(self, soup):
        title = soup.title.string.lower() if soup.title and soup.title.string else ""
        return "index of" in title

    def extract_listing_links(self, soup):
        return [a.get('href') for a in soup.find_all('a', href=True) if a.get('href') and not a.get('href').startswith("?")]

        
class tree:
    def __init__(self, url=None):
        self.url = url

    def update_structure(self, structure, links):
        base_netloc = urlparse(self.url).netloc
        file_extensions = ['.html', '.htm', '.php', '.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.css', '.js', '.json', '.xml', '.txt', '.pdf', '.docx', '.xlsx', '.pptx', '.otf']

        for link in links:
            if not link or ".." in link or "javascript:" in link or "mailto:" in link:
                continue
            
            # Normalize link
            if link.startswith('http'):
                parsed_link = urlparse(link)
                if parsed_link.netloc != base_netloc:
                    continue
                path = parsed_link.path
            else:
                path = urljoin(self.url, link)
                path = urlparse(path).path

            # Check if it's a file
            if any(path.endswith(ext) for ext in file_extensions):
                # It's a file, insert directly under the right branch
                segments = [segment for segment in path.strip('/').split('/') if segment]
                current_level = structure[self.url]
                for seg in segments[:-1]:  # Traverse until parent
                    if seg not in current_level:
                        current_level[seg] = {}
                    current_level = current_level[seg]
                # Insert the file
                if segments[-1] not in current_level:
                    current_level[segments[-1]] = {}
            else:
                # It's a directory
                segments = [segment for segment in path.strip('/').split('/') if segment]
                current_level = structure[self.url]
                for seg in segments:
                    if seg not in current_level:
                        current_level[seg] = {}
                    current_level = current_level[seg]

        return structure

    
def is_responding(url):
    try:
        code, text, time, size = cache.fetch(url)
        return code, text, time, size
    except requests.exceptions.RequestException:
        return None, None, None, None
    
    