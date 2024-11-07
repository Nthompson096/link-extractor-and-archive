import requests
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import urllib3
import re
import argparse

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

def archive_with_archive_ph(url, debug=False):
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
        
        archived_url = extract_archived_url(response.text)
        if archived_url:
            if debug:
                print(f"[DEBUG] Successfully archived: {url} -> {archived_url}")
            return archived_url
        
        return None
    except requests.exceptions.RequestException as e:
        print(f"Failed to archive with Archive.ph: {url}")
        print(f"Error: {e}")
        return None

def extract_archived_url(response_text):
    match = re.search(r'https://archive\.ph/\S+', response_text)
    return match.group(0) if match else None

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Archive URLs using Archive.ph.')
    
    parser.add_argument('file', type=str, help='Path to the text file containing URLs to archive.')
    
    args = parser.parse_args()
    
    urls = []
    
    # Read URLs from the specified file
    try:
        with open(args.file, 'r') as file:
            urls = file.read().splitlines()
    except FileNotFoundError:
        print(f"Error: The file '{args.file}' was not found.")
        return

    # Open results.txt for writing results
    with open("results.txt", "w") as results_file:
        successful_archives = 0
        failed_archives = 0

        # Ask user if they want to enable debugging
        debug_input = input("Enable debugging? (y/n): ").strip().lower()
        debug_mode = debug_input == 'y'

        for url in urls:
            archived_url = archive_with_archive_ph(url, debug=debug_mode)
            
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
