import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import scrolledtext
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import os

def extract_links(url, exclude_words=None):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = []
        for link in soup.find_all('a', href=True):
            full_link = urljoin(url, link['href'])
            if exclude_words and any(excluded_word in full_link for excluded_word in exclude_words):
                continue
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
            cleaned_link = re.sub(r',user$', '', link)  # Remove ',user' if it exists
            f.write(f"{cleaned_link}\n")  # Write cleaned link without username

def overwrite_links_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
    print(f"Cleared existing content in {filename}")

def extract_and_log_links():
    urls = text_input.get("1.0", "end-1c").split()
    exclude_words_input = exclude_input.get("1.0", "end-1c").splitlines()
    
    if not urls:
        messagebox.showwarning("Input Error", "Please enter at least one URL.")
        return
    
    exclude_words = [word.strip() for word in exclude_words_input if word.strip()]

    overwrite_links_file('links.txt')

    all_links = []
    for i, url in enumerate(urls):
        base_url = url.split('?')[0]
        print(f"Extracting links from: {base_url}")
        links = extract_links(base_url, exclude_words)
        all_links.extend(links)
        
        if links:
            mode = 'w' if i == 0 else 'a'
            clean_and_log_links(links, 'links.txt', mode)
        else:
            messagebox.showerror("Error", f"No links found or an error occurred for {url}")

    messagebox.showinfo("Done", f"Total links extracted and cleaned: {len(all_links)}")
    display_log()

def display_log():
    with open('links.txt', 'r') as file:
        log_content = file.read()
        log_text.delete("1.0", tk.END)
        log_text.insert(tk.INSERT, log_content)

def save_as_settings():
    urls = text_input.get("1.0", "end-1c").strip()
    exclude_words = exclude_input.get("1.0", "end-1c").strip()

    if not urls:
        messagebox.showwarning("Input Error", "Please enter URLs before saving.")
        return
    
    # Let the user select a location and filename to save the settings
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    
    if not file_path:
        return  # User canceled the save operation

    with open(file_path, "w") as file:
        file.write(f"URLs:\n{urls}\n")
        if exclude_words:
            file.write(f"Exclude Words:\n{exclude_words}\n")
    
    messagebox.showinfo("Settings Saved", f"Your settings have been saved to {file_path}.")

def load_settings():
    file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    
    if not file_path:
        messagebox.showwarning("Load Error", "No settings file selected.")
        return
    
    if not os.path.exists(file_path):
        messagebox.showwarning("Load Error", "The selected file does not exist.")
        return

    with open(file_path, "r") as file:
        content = file.read().splitlines()

    if len(content) >= 2:
        urls = "\n".join(content[1:content.index("Exclude Words:")]).strip() if "Exclude Words:" in content else "\n".join(content[1:]).strip()
        exclude_words = "\n".join(content[content.index("Exclude Words:") + 1:]).strip() if "Exclude Words:" in content else ""

        text_input.delete("1.0", tk.END)
        exclude_input.delete("1.0", tk.END)
        
        text_input.insert(tk.END, urls)
        exclude_input.insert(tk.END, exclude_words)

    messagebox.showinfo("Settings Loaded", "Your settings have been loaded successfully.")

root = tk.Tk()
root.title("Link Extractor")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

lbl = tk.Label(frame, text="Enter URLs (one per line):")
lbl.pack(anchor="w")

text_input = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50, height=10)
text_input.pack(pady=5)

exclude_lbl = tk.Label(frame, text="Enter words to exclude (one per line) [Optional]:")
exclude_lbl.pack(anchor="w")

exclude_input = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50, height=10)
exclude_input.pack(pady=5)

btn_extract = tk.Button(frame, text="Extract and Log Links", command=extract_and_log_links)
btn_extract.pack(pady=5)

btn_save_as = tk.Button(frame, text="Save Settings As...", command=save_as_settings)
btn_save_as.pack(pady=5)

btn_load = tk.Button(frame, text="Load Settings", command=load_settings)
btn_load.pack(pady=5)

log_label = tk.Label(frame, text="Log Output:")
log_label.pack(anchor="w")

log_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50, height=10)
log_text.pack(pady=5)

root.mainloop()
