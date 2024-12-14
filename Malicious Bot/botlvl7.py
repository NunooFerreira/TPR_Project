import requests
import time
import random
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# List of all the pages to simulate requests
fixed_pages = [
    'http://127.0.0.1/404.html',
    'http://127.0.0.1/about.html',
    'http://127.0.0.1/about3.html',
    'http://127.0.0.1/blog.html',
    'http://127.0.0.1/blog-single.html',
    'http://127.0.0.1/career.html',
    'http://127.0.0.1/comming-soon.html',
    'http://127.0.0.1/contact.html',
    'http://127.0.0.1/FAQ.html',
    'http://127.0.0.1/homepage-2.html',
    'http://127.0.0.1/homepage-3.html',
    'http://127.0.0.1/index.html',
    'http://127.0.0.1/index2.html',
    'http://127.0.0.1/index3.html',
    'http://127.0.0.1/privacy-policy.html',
    'http://127.0.0.1/service.html',
    'http://127.0.0.1/sign-in.html',
    'http://127.0.0.1/sign-up.html',
    'http://127.0.0.1/team.html',
    'http://127.0.0.1/why.html'
]

# Mean and standard deviation for the Gaussian distribution to mimic behavior
mean_interval = 40.25505546  # Average interval in seconds
std_dev_interval = 5  # Standard deviation in seconds

def make_request():
    # Randomly choose one of the fixed pages
    chosen_page = random.choice(fixed_pages)

    # Request the chosen page
    response = requests.get(chosen_page)
    response.raise_for_status()

    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find and request all CSS, JS, and image resources
    resources = []
    for tag in soup.find_all(['link', 'script', 'img']):
        if tag.name == 'link' and tag.get('rel') == ['stylesheet']:
            resource_url = urljoin(chosen_page, tag['href'])
        elif tag.name == 'script' and tag.get('src'):
            resource_url = urljoin(chosen_page, tag['src'])
        elif tag.name == 'img' and tag.get('src'):
            resource_url = urljoin(chosen_page, tag['src'])
        else:
            continue

        resources.append(resource_url)

    # Choose a smaller random subset of resources to make the requests more realistic
    if resources:
        num_requests = max(1, random.randint(1, len(resources) // 2))  # Halve the number of requests
        selected_resources = random.sample(resources, num_requests)

        # Make a request for each selected resource
        for resource_url in selected_resources:
            requests.get(resource_url, timeout=5)

    print(f"Page {chosen_page} and random resources requested successfully.")

while True:
    make_request()

    # Generate a random interval based on a Gaussian distribution
    interval = random.gauss(mean_interval, std_dev_interval)

    # Clamp interval to ensure it's within a reasonable range (e.g., 20 to 60 seconds)
    interval = max(20, min(interval, 60))

    print(f"Waiting for {interval:.2f} seconds before the next request...")
    time.sleep(interval)
