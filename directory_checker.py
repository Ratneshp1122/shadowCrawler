import requests

def is_directory_listing(response_text):
    return "Index of /" in response_text or "<title>Index of" in response_text

def check_directories(domain, paths, timeout=5):
    valid_dirs = []

    for path in paths:
        url = f"http://{domain}/{path}".replace("//", "/").replace(":/", "://")
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                listing = is_directory_listing(response.text)
                valid_dirs.append({
                    "url": url,
                    "status_code": 200,
                    "directory_listing": listing
                })
                print(f"[+] 200 OK: {url} {'[Directory Listing]' if listing else ''}")
            elif response.status_code in [403, 401]:
                print(f"[!] {response.status_code} Forbidden/Unauthorized: {url}")
            elif response.status_code == 500:
                print(f"[-] 500 Internal Server Error: {url}")
            else:
                print(f"[-] {response.status_code}: {url}")
        except requests.exceptions.RequestException as e:
            print(f"[x] Request failed for {url}: {str(e)}")
    
    return valid_dirs
