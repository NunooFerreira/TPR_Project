import requests
import time
import random
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# List of all pages to simulate navigation
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

# Function to calculate reading time based on text content
#Uses an average reading speed of ~230 words per minute (common benchmark) pelo google.
def calculate_reading_time(page_url):
    try:
        # Fetch the page content
        response = requests.get(page_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract visible text
        for tag in soup(['script', 'style']):
            tag.decompose()  # Remove script and style tags
        text = soup.get_text(separator=' ')
        
        # Calculate word count
        words = text.split()
        word_count = len(words)
        
        # Estimate reading time
        average_reading_speed = 230  # Words per minute
        estimated_time = word_count / average_reading_speed * 60  # Convert minutes to seconds

        # Add a small buffer for scrolling and interaction
        estimated_time += random.uniform(5, 10)  # Add 5-10 seconds buffer
        return round(estimated_time, 2)

    except Exception as e:
        print(f"Error calculating reading time for {page_url}: {e}")
        return random.uniform(20, 60)  # Fallback to random estimate

# Function to simulate a single page request
def make_request(current_page):
    try:
        # Request the page
        response = requests.get(current_page)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        print(f"Visiting: {current_page}")

        # Calculate reading time dynamically
        reading_time = calculate_reading_time(current_page)
        print(f"Estimated reading time for {current_page}: {reading_time:.2f}s")

        # Emulate scrolling behavior
        scroll_delay = reading_time / 4  # Divide time into 4 scroll sections
        for _ in range(4):
            print(f"Scrolling... ({scroll_delay:.2f}s delay)")
            time.sleep(scroll_delay)  # Pause for scrolling

        # Extract internal links
        internal_links = [
            urljoin(current_page, tag['href'])
            for tag in soup.find_all('a', href=True)
            if urljoin(current_page, tag['href']).startswith('http://127.0.0.1')
        ]
        return internal_links
    except Exception as e:
        print(f"Error visiting {current_page}: {e}")
        return []

# Function to simulate sequential page navigation
def sequential_navigation(start_page):
    visited_pages = set()  # Keep track of visited pages to avoid cycles
    pages_to_visit = [start_page]

    while pages_to_visit:
        current_page = pages_to_visit.pop(0)

        if current_page in visited_pages:
            continue  # Skip already visited pages

        visited_pages.add(current_page)

        # Visit the current page and get internal links
        internal_links = make_request(current_page)
        
        # Randomly shuffle internal links for variation
        random.shuffle(internal_links)

        # Add unvisited links to the queue
        for link in internal_links:
            if link not in visited_pages:
                pages_to_visit.append(link)

        # Introduce a realistic delay between navigation
        navigation_delay = random.uniform(20, 40)  # Wait 20-40 seconds before the next page
        print(f"Waiting {navigation_delay:.2f} seconds before navigating to the next page...")
        time.sleep(navigation_delay)

# Start the bot with a random page
start_page = random.choice(fixed_pages)
sequential_navigation(start_page)
