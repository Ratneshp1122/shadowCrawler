import subdomainExtract
import requests
import time
from directory_checker import check_directories
from crrawler import crawl



def check_directory_listing(domain, path):
    full_url = f"http://{domain}{path}"
    try:
        response = requests.get(full_url, timeout=10)
        if response.status_code == 200 and ("Index of" in response.text or "<title>Index" in response.text or "<h1>Index of" in response.text):
            print(f"[!] Directory Listing Found: {full_url}")
            return True
    except requests.RequestException:
        pass
    print(f"[-] Failed to check directory listing: {full_url}")
    return False

if __name__ == "__main__":
    paths = ["admin/", "backup/", "images/", "index.php", "wp-content/uploads/"]
    results = check_directories("testphp.vulnweb.com", paths,timeout=15)
    print(results[:10])

    paths = crawl("testphp.vulnweb.com", max_depth=1)
    print(paths)



    domain = input("[*] Enter domain name: ")
    paths = subdomainExtract.get_paths(domain)[:50]  
    with open ("paths.txt", "w") as f:
        f.write("\n".join(paths))

    print(f"[+] Saved {len(paths)} paths to paths.txt")

    print(f"[+] Checking directory listings on {domain}...\n")
    for i,path in enumerate(paths):
        check_directory_listing(domain, path)
        time.sleep(0.3)
