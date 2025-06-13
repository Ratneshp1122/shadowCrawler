import requests

def load_wordList(file_path):
    try:
        with open(file_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            print(f"[DEBUG] Loaded {len(lines)} entries from {file_path}")
            return lines
    except FileNotFoundError:
        print("[!] wordList not found.")
        return []

def brute_force_directories(domain, wordList_file="wordList.txt"):
    base_url = f"http://{domain}"
    lines = load_wordList(wordList_file)
    found_dirs = []

    print(f"[*] Starting directory bruteforce on {base_url}")
    for path in lines:
        full_url = f"{base_url}/{path}"
        try:
            response = requests.get(full_url, timeout=5, allow_redirects=False)
            print(f"[DEBUG] Checked: {full_url} => {response.status_code}")
            if response.status_code in [200, 301, 302, 403]:
                found_dirs.append(full_url)
        except requests.RequestException as e:
            print(f"[!] Error checking {full_url}: {e}")

    return found_dirs

if __name__ == "__main__":
    domain = input("[*] Enter domain (e.g., example.com): ").strip()
    found = brute_force_directories(domain)
    if found:
        print("\n[+] Discovered Directories:")
        for url in found:
            print("  -", url)
    else:
        print("[!] No directories found.")
