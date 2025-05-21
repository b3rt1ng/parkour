
import requests
import socket
import argparse
from time import time
from random import randint
from bs4 import BeautifulSoup
from src.utils import Utils
from src.mapper import page_mapper, tree

begin = time()
parser = argparse.ArgumentParser(description="Scan a website and display its structure.")
parser.add_argument("url", type=str, help="The URL of the website to scan.")
parser.add_argument("-f", "--full", action="store_true", help="Display the full link for each path printing.")
parser.add_argument("-k", "--keyword", type=str, help="Comma-separated keywords to look for in pages.")
parser.add_argument("-r", "--response", action="store_true", help="Try to get the response code of each link.")

args = parser.parse_args()

utils = Utils()

keywords = args.keyword
if keywords:
    keywords_colored = [utils.colored_text(keyword, utils.random_color()) for keyword in keywords.split(",")]
    keywords = keywords.split(",")
    print("Will look for: [", end="")
    for keyword in keywords_colored:
        print(f"{keyword}", end=(", " if keyword != keywords_colored[-1] else ""))
    print("]")

def only_url(url):
    if url.startswith("http://"):
        url = url[7:]
    elif url.startswith("https://"):
        url = url[8:]
    return url.split("/")[0]

def get_page(url):
    req = requests.get(url)
    if req.status_code == 200:
        return req.text
    else:
        print(f"Error: {req.status_code}")
        return None

url = args.url

if not args.response:
    print(utils.gradient_text("Warning: The response code of each link will not be checked !\nthe scan will be quicker but will not check for keywords, nor further analyse the links.\nIf you want to check the response code of each link, use -r or --response.\n",start_color=(255, 0, 0), end_color=(255, 255, 0)))

print(f"scanning {utils.gradient_text(url)}")
try:
    print("website IP:",utils.gradient_text(socket.gethostbyname(only_url(url))))
except socket.gaierror:
    print("Error: Unable to resolve the domain name.")
    
website = {url: {}}
page = get_page(url)
print("Page title:", utils.gradient_text(utils.get_title(page)))

mapper = page_mapper(url)
links = mapper.get_links()
website = tree(url).update_structure(website, links)

print(utils.gradient_text("Main server"))

try:
    utils.print_dict_tree(website, args.full, keywords=keywords, check_response=args.response)
except KeyboardInterrupt:
    print(utils.colored_text("\nStopping the scan...", (255, 0, 0)))
    exit(0)

end = time()
time_amount = end - begin
print(f"\nScan completed in {utils.colored_text(time_amount, (100, 255, 100))} seconds.")

