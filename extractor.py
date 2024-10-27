import requests
from bs4 import BeautifulSoup
import argparse

def extract_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = []
        for link in soup.find_all('a', href=True):
            links.append(link['href'])
        
        return links
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []

def log_links_to_file(links, filename):
    with open(filename, 'w') as file:
        for link in links:
            file.write(link + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract links from a website")
    parser.add_argument("--weburl", help="URL of the website to extract links from", required=True)
    args = parser.parse_args()

    url = args.weburl
    links = extract_links(url)
    
    if links:
        log_links_to_file(links, 'links.txt')
        print(f"Links have been logged to links.txt")
    else:
        print("No links found or an error occurred.")
