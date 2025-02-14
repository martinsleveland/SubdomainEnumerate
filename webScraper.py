import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

# Target website (use responsibly!)
TARGET_URL = input("Enter the target URL (example: https://sleveland.xyz): ")

# List of sensitive keywords to scan for
SENSITIVE_KEYWORDS = ["password", "apikey", "secret", "token"]

# Common outdated software versions
OUTDATED_SOFTWARE = {
    'WordPress': '5.8',
    'Joomla': '3.9',
    'Drupal': '8.8',
    'Moodle': '3.10',
    'PHP': '7.4',
}

def get_links(url):
    """Extract all links from a webpage."""
    links = set()
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        
        for link in soup.find_all("a", href=True):
            full_url = urljoin(url, link["href"])
            if full_url.startswith(TARGET_URL):  # Only crawl the target site
                links.add(full_url)
    except requests.exceptions.RequestException:
        pass
    
    return links

def scan_page(url):
    """Scan a webpage for vulnerabilities."""
    print(f"Scanning: {url}")
    
    try:
        response = requests.get(url, timeout=5)
        page_text = response.text.lower()
        
        # Check for sensitive keywords
        for keyword in SENSITIVE_KEYWORDS:
            if keyword in page_text:
                print(f"⚠️ Possible exposed {keyword} found on {url}")

        # Detect outdated software versions
        for software, old_version in OUTDATED_SOFTWARE.items():
            if f"{software.lower()} {old_version}" in page_text:
                print(f"⚠️ Outdated {software} version {old_version} found on {url}")

        # Detect email addresses (potential leaks)
        emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", page_text)
        if emails:
            print(f"[+] Found email addresses: {emails}")
        
    except requests.exceptions.RequestException:
        print(f"[-] Could not access {url}")

def main():
    """Main function to start scanning."""
    print(f"Starting scan on {TARGET_URL}...\n")
    
    scanned_urls = set()
    to_scan = {TARGET_URL}

    while to_scan:
        url = to_scan.pop()
        if url not in scanned_urls:
            scanned_urls.add(url)
            scan_page(url)
            to_scan.update(get_links(url) - scanned_urls)

    print("\n[+] Scan complete!")

if __name__ == "__main__":
    main()
