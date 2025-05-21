import re

def get_simple_url(text):
    # regex to find url
    regex = r'(https?://[^\s]+)'
    match = re.search(regex, text)
    if match:
        url = match.group(0)
        # remove http:// or https://
        url = url.replace("http://", "").replace("https://", "")
        # remove trailing slash
        url = url.rstrip("/")
        return url
    return None