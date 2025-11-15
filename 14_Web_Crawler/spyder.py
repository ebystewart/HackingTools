import requests
import re
from urllib.parse import urljoin
from urllib.parse import urlparse

target_url = "http://192.168.1.9/mutillidae"
target_links = []

def extract_links_from(url):
    response = requests.get(target_url)
    #print(response.content)
    return re.findall('(?:href=")(.*?)"', response.content.decode(errors="ignore"))


def crawl(url):
    href_links = extract_links_from(url)
    #print(href_links)
    for link in href_links:
        refactored_link = urljoin(url, link)

        if "#" in link:
            refactored_link = refactored_link.split("#")[0]

        if target_url in refactored_link and refactored_link not in target_links:
            target_links.append(refactored_link)
            print(refactored_link)
            # This is not protected against recursive web page links (web pages linked recursively)
            crawl(refactored_link) # recurse through each link found

def store_result(file_path):
    with open(file_path, "w") as file:
        for item in target_links:
            file.write(f"{item}\n")

crawl(target_url)
store_result("nw_map.txt")