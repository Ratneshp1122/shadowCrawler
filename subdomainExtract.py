import waybackcdx
import re
from urllib.parse import urlparse


def is_probable_directory(path):
    return path.endswith("/") and len(path) < 100 and not re.search(r"\.\w{2,5}$", path)

def get_paths(domain):
    urls = waybackcdx.fetch_wayback_urls(domain)
    print(f"[+] Extracting paths from {len(urls)} URLs...")
    
    paths = set()
    for url in urls:
        try:
            # Remove domain
            path = url.split(domain, 1)[-1]
            if not path.startswith("/"):
                path = "/" + path
            if path.count("/") > 1 and len(path) < 100 and is_probable_directory(path):
                if (":80" in path) or (":443" in path):
                    continue
                else:
                    paths.add(path.split("?")[0])  # remove query strings

        except Exception as e:
            continue

    print(f"[+] Extracted {len(paths)} unique paths.")
    return list(paths)

# For testing
if __name__ == "__main__":
    domain = "testphp.vulnweb.com"
    paths = get_paths(domain)
    print(paths[:10])  # show sample
