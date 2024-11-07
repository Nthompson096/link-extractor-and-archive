from flask import Flask, render_template, request, jsonify, send_file
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract():
    url = request.form['url']
    links = extract_links(url)
    
    # Extract usernames but do not include them in the written links
    usernames = [extract_username(link) for link in links]
    
    with open('links.txt', 'w') as f:
        for link, username in zip(links, usernames):
            # Remove the username from the link if it exists
            cleaned_link = link.split(',')[0]  # Keep only the part before ',user'
            f.write(f"{cleaned_link}\n")  # Write cleaned link without username
    
    return jsonify(links=links, usernames=usernames)

@app.route('/download_links')
def download_links():
    return send_file('links.txt', as_attachment=True)

@app.route('/website/<username>')
def user_profile(username):
    full_url = url_for('user_profile', username=username, _external=True)
    query_params = request.args.to_dict()
    if query_params:
        full_url += '?' + '&'.join([f"{k}={v}" for k, v in query_params.items()])
    return full_url

@app.route('/get_full_link/<username>')
def get_full_link(username):
    full_url = url_for('user_profile', username=username, _external=True) + '?o=0'
    return jsonify(full_link=full_url)

if __name__ == '__main__':
    app.run(debug=True)
