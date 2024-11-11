import requests
from bs4 import BeautifulSoup
import argparse
from urllib.parse import urljoin, urlparse
import re
import os

        # Print the ASCII art
print("""
 ██▓     ██▓ ███▄    █  ██ ▄█▀   ▓█████ ▒██   ██▒▄▄▄█████▓ ██▀███   ▄▄▄       ▄████▄  ▄▄▄█████▓ ▒█████   ██▀███  
▓██▒    ▓██▒ ██ ▀█   █  ██▄█▒    ▓█   ▀ ▒▒ █ █ ▒░▓  ██▒ ▓▒▓██ ▒ ██▒▒████▄    ▒██▀ ▀█  ▓  ██▒ ▓▒▒██▒  ██▒▓██ ▒ ██▒
▒██░    ▒██▒▓██  ▀█ ██▒▓███▄░    ▒███   ░░  █   ░▒ ▓██░ ▒░▓██ ░▄█ ▒▒██  ▀█▄  ▒▓█    ▄ ▒ ▓██░ ▒░▒██░  ██▒▓██ ░▄█ ▒
▒██░    ░██░▓██▒  ▐▌██▒▓██ █▄    ▒▓█  ▄  ░ █ █ ▒ ░ ▓██▓ ░ ▒██▀▀█▄  ░██▄▄▄▄██ ▒▓▓▄ ▄██▒░ ▓██▓ ░ ▒██   ██░▒██▀▀█▄  
░██████▒░██░▒██░   ▓██░▒██▒ █▄   ░▒████▒▒██▒ ▒██▒  ▒██▒ ░ ░██▓ ▒██▒ ▓█   ▓██▒▒ ▓███▀ ░  ▒██▒ ░ ░ ████▓▒░░██▓ ▒██▒
░ ▒░▓  ░░▓  ░ ▒░   ▒ ▒ ▒ ▒▒ ▓▒   ░░ ▒░ ░▒▒ ░ ░▓ ░  ▒ ░░   ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░░ ░▒ ▒  ░  ▒ ░░   ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░
░ ░ ▒  ░ ▒ ░░ ░░   ░ ▒░░ ░▒ ▒░    ░ ░  ░░░   ░▒ ░    ░      ░▒ ░ ▒░  ▒   ▒▒ ░  ░  ▒       ░      ░ ▒ ▒░   ░▒ ░ ▒░
  ░ ░    ▒ ░   ░   ░ ░ ░ ░░ ░       ░    ░    ░    ░        ░░   ░   ░   ▒   ░          ░      ░ ░ ░ ▒    ░░   ░ 
    ░  ░ ░           ░ ░  ░         ░  ░ ░    ░              ░           ░  ░░ ░                   ░ ░     ░     
                                                                             ░                                   
""")

def extract_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = []
        for link in soup.find_all('a', href=True):
            full_link = urljoin(url, link['href'])
            links.append(full_link)
        
        return links
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL {url}: {e}")
        return []

def extract_username(url):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    
    username_patterns = [
        r'/user/(\w+)',
        r'/profile/(\w+)',
        r'/(\w+)$'
    ]
    
    for pattern in username_patterns:
        match = re.search(pattern, parsed_url.path)
        if match:
            return match.group(1)
    
    for part in reversed(path_parts):
        if part:
            return part
    
    return None

def clean_and_log_links(links, filename, mode='a'):
    usernames = [extract_username(link) for link in links]
    
    with open(filename, mode) as f:
        for link, username in zip(links, usernames):
            # Remove the username from the link if it exists
            cleaned_link = link.split(',')[0]  # Keep only the part before ',user'
            f.write(f"{cleaned_link}\n")  # Write cleaned link without username

def overwrite_links_file(filename):
    # This function will overwrite the file if it exists
    if os.path.exists(filename):
        os.remove(filename)
    print(f"Cleared existing content in {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract and clean links from multiple websites")
    parser.add_argument("--weburls", nargs='+', help="URLs of the websites to extract links from", required=True)
    args = parser.parse_args()

    # List of URLs to extract links from
    urls = args.weburls

    # Overwrite the links.txt file before starting
    overwrite_links_file('links.txt')

    all_links = []
    for i, url in enumerate(urls):
        print(f"Extracting links from: {url}")
        links = extract_links(url)
        all_links.extend(links)
        
        if links:
            # Use 'w' mode for the first URL, 'a' for the rest
            mode = 'w' if i == 0 else 'a'
            clean_and_log_links(links, 'links.txt', mode)
            print(f"Cleaned links from {url} have been logged to links.txt")
        else:
            print(f"No links found or an error occurred for {url}")

    print(f"Total links extracted and cleaned: {len(all_links)}")
