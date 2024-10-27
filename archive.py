import requests
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504)):
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def archive_url(url):
    archive_url = "https://archive.ph/submit/"
    payload = {
        "url": url,
        "capture_all": "on"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests_retry_session().post(
            archive_url, 
            data=payload, 
            headers=headers, 
            timeout=60,
            verify=False  # Disable SSL verification
        )
        response.raise_for_status()
        print(f"Successfully archived: {url}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Failed to archive: {url}")
        print(f"Error: {e}")
        return False

def main():
    # Read URLs from links.txt
    with open("links.txt", "r") as file:
        urls = file.read().splitlines()

    # Archive each URL
    successful_archives = 0
    failed_archives = 0

    for url in urls:
        if archive_url(url):
            successful_archives += 1
        else:
            failed_archives += 1
        time.sleep(60)  # Wait 10 seconds between requests

    print(f"\nArchiving complete.")
    print(f"Successfully archived: {successful_archives}")
    print(f"Failed to archive: {failed_archives}")

if __name__ == "__main__":
    main()