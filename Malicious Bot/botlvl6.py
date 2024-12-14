import requests
import time
import random
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

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

# Gaussian distribution parameters for request intervals
mean_interval = 10  # Average interval in seconds
std_dev_interval = 2  # Standard deviation in seconds

# Weighted probabilities for resource types
weights = {'css': 0.4, 'js': 0.3, 'img': 0.3}

# Dynamic interval calculation based on silence metrics
def calculate_dynamic_interval(silence_count, total_silence_time):
    base_interval = total_silence_time / max(1, silence_count)  # Avoid division by zero
    noise = random.gauss(0, 2)  # Add small Gaussian noise
    return max(2, base_interval + noise)

# Determine bot profile based on silence count
def get_bot_profile(silence_count):
    if silence_count > 50:
        return "stealthy"
    elif silence_count < 20:
        return "aggressive"
    return "random"

# Adjust interval parameters based on bot profile
def adjust_intervals_by_profile(profile):
    global mean_interval, std_dev_interval
    if profile == "stealthy":
        mean_interval = 20
        std_dev_interval = 5
    elif profile == "aggressive":
        mean_interval = 5
        std_dev_interval = 2
    else:  # Random profile
        mean_interval = random.choice([10, 15, 20])
        std_dev_interval = 3

while True:
    # Simulated metrics for silence (these should be dynamically updated in real scenarios)
    silence_count = random.randint(10, 60)  # Example simulated value
    total_silence_time = random.randint(100, 300)  # Example simulated value

    # Log silence metrics
    logging.info(f"SilenceCount: {silence_count}, TotalSilenceTime: {total_silence_time}")

    # Determine bot profile and adjust intervals
    profile = get_bot_profile(silence_count)
    adjust_intervals_by_profile(profile)

    # Randomly choose one of the fixed pages
    chosen_page = random.choice(fixed_pages)

    # Request the chosen page
    try:
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

        # Select resources to request based on weighted probabilities
        selected_resources = []
        for resource_url in resources:
            resource_type = (
                'css' if '.css' in resource_url else
                'js' if '.js' in resource_url else
                'img'
            )
            if random.random() < weights[resource_type]:
                selected_resources.append(resource_url)

        # Request a random subset of the selected resources
        for resource_url in random.sample(selected_resources, random.randint(1, len(selected_resources))):
            requests.get(resource_url, timeout=5)

        logging.info(f"Page {chosen_page} and random resources requested successfully.")

    except requests.RequestException as e:
        logging.error(f"Failed to request {chosen_page}: {e}")

    # Generate a dynamic interval based on silence metrics
    interval = calculate_dynamic_interval(silence_count, total_silence_time)
    logging.info(f"Waiting for {interval:.2f} seconds before the next request...")
    time.sleep(interval)
