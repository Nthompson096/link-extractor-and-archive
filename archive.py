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
        
        # Extract the archived URL from the response
        archived_url = extract_archived_url(response.text)
        if archived_url:
            print(f"Successfully archived: {url}")
            print(f"Archived URL: {archived_url}")
            return archived_url
        
        return None
    except requests.exceptions.RequestException as e:
        print(f"Failed to archive: {url}")
        print(f"Error: {e}")
        return None

def extract_archived_url(response_text):
    # This is a placeholder for extracting the archived URL from the response text.
    import re
    match = re.search(r'https://archive\.ph/\S+', response_text)
    return match.group(0) if match else None

def main():
    # Read URLs from links.txt
    with open("links.txt", "r") as file:
        urls = file.read().splitlines()

    # Open results.txt for writing results
    with open("results.txt", "w") as results_file:
        successful_archives = 0
        failed_archives = 0

        for url in urls:
            archived_url = archive_url(url)
            if archived_url:
                results_file.write(f"Original URL: {url}\nArchived URL: {archived_url}\n\n")
                successful_archives += 1
            else:
                failed_archives += 1
            
            time.sleep(10)  # Wait 10 seconds between requests

        print(f"\nArchiving complete.")
        print(f"Successfully archived: {successful_archives}")
        print(f"Failed to archive: {failed_archives}")

if __name__ == "__main__":
    main()
