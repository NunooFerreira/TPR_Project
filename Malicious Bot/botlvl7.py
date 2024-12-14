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

# Values derived from your CSV
avg_num_requests = 3.716071429  # Avg requests per minute
avg_requests_js = 1.1
avg_requests_html = 0.589285714
avg_requests_css = 0.057142857
avg_response_size = 97056.74107
avg_image_size = 89691.53036
avg_silence_time = 44.8030303

# Simulation duration (in seconds)
window_duration = 300  # 5 minutes

def make_request(url):
    """Make a request and return the response size."""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return len(response.content)
    except requests.RequestException as e:
        print(f"Error requesting {url}: {e}")
        return 0

def simulate_user_behavior():
    """Simulate user behavior based on the metrics."""
    start_time = time.time()

    # Track requests to meet averages
    total_requests = 0
    js_requests = 0
    html_requests = 0
    css_requests = 0
    total_response_size = 0

    while time.time() - start_time < window_duration:
        # Choose a random page to request
        chosen_page = random.choice(fixed_pages)
        response_size = make_request(chosen_page)
        total_requests += 1
        total_response_size += response_size

        # Parse the page content using BeautifulSoup
        response = requests.get(chosen_page)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Simulate resource requests based on averages
        resources = []
        for tag in soup.find_all(['link', 'script', 'img']):
            if tag.name == 'link' and tag.get('rel') == ['stylesheet']:
                if css_requests < avg_requests_css * window_duration / 60:
                    resource_url = urljoin(chosen_page, tag['href'])
                    resources.append(resource_url)
                    css_requests += 1
            elif tag.name == 'script' and tag.get('src'):
                if js_requests < avg_requests_js * window_duration / 60:
                    resource_url = urljoin(chosen_page, tag['src'])
                    resources.append(resource_url)
                    js_requests += 1
            elif tag.name == 'img' and tag.get('src'):
                if html_requests < avg_requests_html * window_duration / 60:
                    resource_url = urljoin(chosen_page, tag['src'])
                    resources.append(resource_url)
                    html_requests += 1

        # Make requests for the resources
        for resource_url in resources:
            total_response_size += make_request(resource_url)

        # Wait for the average silence time between requests
        time.sleep(avg_silence_time / 60)

    print(f"Simulation completed: {total_requests} requests made.")
    print(f"Total response size: {total_response_size} bytes.")

# Start the simulation
simulate_user_behavior()
