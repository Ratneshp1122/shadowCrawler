import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import time

visited = set()

def is_valid(url, base_domain):
    parsed = urlparse(url)
    if parsed.scheme not in ["http", "https"]:
        return False
    if parsed.netloc and base_domain not in parsed.netloc:
        return False
    if url.startswith("mailto:") or url.startswith("javascript:") or url.startswith("#"):
        return False
    return True

def extract_links(url):
    try:
        response = requests.get(url, timeout=10)
        if not response.headers.get("content-type", "").startswith("text/html"):
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        links = set()
        for tag in soup.find_all("a", href=True):
            href = tag['href'].strip()
            joined_url = urljoin(url, href)
            links.add(joined_url.split("#")[0])
        return links

    except requests.RequestException as e:
        print(f"[!] Error fetching {url}: {e}")
        return []

def crawl(base_url, depth=2):
    base_domain = urlparse(base_url).netloc
    to_visit = {base_url}
    all_links = set()

    for _ in range(depth):
        next_round = set()
        for current_url in to_visit:
            if current_url in visited:
                continue
            visited.add(current_url)

            print(f"[*] Crawling: {current_url}")
            links = extract_links(current_url)

            for link in links:
                if is_valid(link, base_domain) and link not in visited:
                    all_links.add(link)
                    next_round.add(link)

            time.sleep(0.5)  # polite crawling
        to_visit = next_round

    return sorted(all_links)

if __name__ == "__main__":
    domain = input("[*] Enter domain (e.g., testphp.vulnweb.com): ").strip()
    base_url = f"http://{domain}"
    links = crawl(base_url)

    if links:
        print("\n[+] Discovered URLs:")
        for link in links:
            print("  -", link)
    else:
        print("[!] No links found.")
