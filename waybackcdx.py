import requests
import time
import json
import os

def fetch_wayback_urls(domain, use_cache=True):
    url = f"https://web.archive.org/cdx/search/cdx?url={domain}/*&output=json&fl=original&collapse=urlkey"
    cache_file = f"{domain.replace('.', '_')}_cdx.json"

    # Serve from cache if available
    if use_cache and os.path.exists(cache_file):
        print(f"[+] Loaded cached data for: {domain}")
        with open(cache_file, 'r') as f:
            data = json.load(f)
        return [entry[0] for entry in data[1:]]  # Skip header

    print(f"[+] Fetching archive URLs for: {domain}")

    # Retry logic
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            with open(cache_file, 'w') as f:
                f.write(response.text)

            data = response.json()
            print(f"[+] Found {len(data) - 1} URLs.")
            return [entry[0] for entry in data[1:]]  # Skip header

        except requests.exceptions.RequestException as e:
            print(f"[!] Attempt {attempt+1}/3 failed: {e}")
            time.sleep(3)

    print("[-] All attempts to fetch Wayback URLs failed.")
    return []

if __name__ == "__main__":
    domain = input("[*] Enter domain name: ")
    old_urls = fetch_wayback_urls(domain)
    print(old_urls[:10])

