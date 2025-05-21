# This class is used to process the webpage content in order to get
# the links and the title of the page.

import re
from random import randint
import json
import requests
from .mapper import is_responding
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from .http_cache import PageCache

class Utils:
    def __init__(self):
        self._rdmcolor = False
        self.display_art()
        self.cache = PageCache()
        pass

    def get_title(self, page):
        title = re.search(r'<title>(.*?)</title>', page, re.IGNORECASE)
        if title:
            return title.group(1)
        else:
            return None

    def gradient_text(self, text, start_color=(255, 255, 0), end_color=(0, 255, 255), random_color=False):
        result = ""
        length = len(text)
        if random_color:
            start_color = self.random_color()
            end_color = self.random_color()
        for i, char in enumerate(text):
            ratio = i / max(length - 1, 1)
            r = int(start_color[0] + ratio * (end_color[0] - start_color[0]))
            g = int(start_color[1] + ratio * (end_color[1] - start_color[1]))
            b = int(start_color[2] + ratio * (end_color[2] - start_color[2]))
            # Add the colored character
            result += f"\033[38;2;{r};{g};{b}m{char}"
        result += "\033[0m"
        return result
    
    def colored_text(self, text, foreground_color=(255, 255, 255), background_color=None):
        r, g, b = foreground_color
        if background_color:
            bg_r, bg_g, bg_b = background_color
            return f"\033[38;2;{r};{g};{b}m\033[48;2;{bg_r};{bg_g};{bg_b}m{text}\033[0m"
        else:
            return f"\033[38;2;{r};{g};{b}m{text}\033[0m"
        
    def find_text_content(self, html, keywords=list):
        dict = {}
        soup = BeautifulSoup(html, 'html.parser' if '<html' in html.lower() else 'xml')
        for keyword in keywords:
            # Find all occurrences of the keyword in the text
            occurrences = soup(text=re.compile(keyword, re.IGNORECASE))
            if occurrences:
                dict[keyword] = len(occurrences)
        return dict

    

    def random_color(self):
        base = 127  # Base pastel (moitié de 255)
        return (
            randint(base, 255),
            randint(base, 255),
            randint(base, 255)
        )

    def display_art(self):
        art = r"""
▗▄▄▖ ▗▞▀▜▌ ▄▄▄ █  ▄  ▄▄▄  █  ▐▌ ▄▄▄                 _
▐▌ ▐▌▝▚▄▟▌█    █▄▀  █   █ ▀▄▄▞▘█                  _( }
▐▛▀▘      █    █ ▀▄ ▀▄▄▄▀      █        -=   _  <<  \
▐▌             █  █                         `.\__/`/\\
                                      -=      '--'\\  `
               By @B3rt1ng                 -=     //
                                                  \)
"""
        red = (255, 0, 0)
        blue = (0, 0, 255)
        print(self.gradient_text(art, red, blue))

    def print_dict(self, d):
        print(json.dumps(d, indent=4))

    def clean_url_join(self, base, key):
        if re.match(r'^https?://', key):
            return key  # key est une URL complète
        if base.endswith('/'):
            base = base[:-1]
        if key.startswith('/'):
            key = key[1:]
        return f"{base}/{key}"
    
    def colorize_status(self, status):
        bg = (10, 10, 10)
        if status is None:
            return "[✗]"
        if 200 <= status < 300:
            return f"[{self.colored_text(status, (180, 255, 180), bg)}]"
        elif 300 <= status < 400:
            return f"[{self.colored_text(status, (255, 255, 180), bg)}]"
        elif 400 <= status < 500:
            return f"[{self.colored_text(status, (255, 180, 180), bg)}]"
        elif 500 <= status < 600:
            return f"[{self.colored_text(status, (255, 180, 255), bg)}]"
        else:
            return f"[{status}]"

    def pretty_dict_numbers(self, d):
        if d == {}:
            return ""
        result = "["
        for key, value in d.items():
            if isinstance(value, int):
                result += f"{key}: {self.colored_text(value, self.random_color(),)}x, "
            else:
                result += f"{self.colored_text(key, self.random_color())}, "
        result = result[:-2] + "]"
        result = self.colored_text(result, foreground_color=(255, 255, 255), background_color=(0, 0, 0))
        return result

    def print_dict_tree(self, data, full, prefix="", path="", keywords=None, check_response=True):
        urls_to_check = []
        full_paths = {}

        for key in data:
            full_path = self.clean_url_join(path, key) if path else key
            full_paths[key] = full_path
            if check_response and full_path.startswith("http"):
                urls_to_check.append(full_path)

        responses = self.batch_check(urls_to_check) if check_response else {}

        for index, (key, value) in enumerate(data.items()):
            full_path = full_paths[key]
            response_data = responses.get(full_path, (None, None, None, None))
            status, content, time, size = response_data
            display_key = full_path if full else key

            pointer = self.gradient_text("└── ") if index == len(data) - 1 else self.gradient_text("├── ")
            keywords_found = self.pretty_dict_numbers(self.find_text_content(content, keywords)) if (keywords and content) else ""

            print(prefix + pointer + display_key + " " + self.colorize_status(status) + keywords_found,
                self.colored_text((f"{size}B" if size else ""), (170, 170, 0), (0, 0, 0)) +
                (f" {time:.2f}s" if time else ""))

            if isinstance(value, dict) and value:
                extension = "    " if index == len(data) - 1 else self.gradient_text("│   ")
                self.print_dict_tree(value, full, prefix + extension, full_path, keywords, check_response)


    def batch_check(self, urls):
        results = {}
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(self.cache.fetch, url): url for url in urls}
            for future in futures:
                url = futures[future]
                results[url] = future.result()
        return results
    
