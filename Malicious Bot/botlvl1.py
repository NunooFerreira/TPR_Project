import requests
import time
import random
from urllib.parse import urljoin
from bs4 import BeautifulSoup

base_url = 'http://127.0.0.1/index.html'

interval = 7

while True:
    # Request the main page
    response = requests.get(base_url)

    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all CSS, JS, and image resources
    resources = []
    for tag in soup.find_all(['link', 'script', 'img']):
        if tag.name == 'link' and tag.get('rel') == ['stylesheet']:
            resource_url = urljoin(base_url, tag['href'])
        elif tag.name == 'script' and tag.get('src'):
            resource_url = urljoin(base_url, tag['src'])
        elif tag.name == 'img' and tag.get('src'):
            resource_url = urljoin(base_url, tag['src'])
        else:
            continue

        resources.append(resource_url)

    # Choose a random subset of resources to request
    num_requests = random.randint(1, len(resources))  # Random number of resources to request
    selected_resources = random.sample(resources, num_requests)

    # Make a request for each selected resource
    for resource_url in selected_resources:
        requests.get(resource_url, timeout=5)

    print("Random subset of resources requested successfully.")
    print(f"Waiting for {interval} seconds before the next request...")
    time.sleep(interval)
