import requests
from bs4 import BeautifulSoup
import argparse
from urllib.parse import urljoin, urlparse
import re

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
        print(f"Error fetching the URL: {e}")
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

def clean_and_log_links(links, filename):
    usernames = [extract_username(link) for link in links]
    
    with open(filename, 'w') as f:
        for link, username in zip(links, usernames):
            # Remove the username from the link if it exists
            cleaned_link = link.split(',')[0]  # Keep only the part before ',user'
            f.write(f"{cleaned_link}\n")  # Write cleaned link without username

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract and clean links from a website")
    parser.add_argument("--weburl", help="URL of the website to extract links from", required=True)
    args = parser.parse_args()

    url = args.weburl
    links = extract_links(url)
    
    if links:
        clean_and_log_links(links, 'links.txt')
        print(f"Cleaned links have been logged to links.txt")
    else:
        print("No links found or an error occurred.")
