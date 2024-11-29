import time
import requests
import random

#Repeatedly request a random page every random seconds (using random agents)

# File containing the list of HTML pages (including JS, CSS, images, etc.)
pages_file = "resources/htmlpages.txt"

# URL of the website (Apache server running locally)
base_url = "http://127.0.0.1"

# Read the page names from the file
try:
    with open(pages_file, "r") as file:
        page_names = [line.strip() for line in file if line.strip()]
except FileNotFoundError:
    print(f"Error: File '{pages_file}' not found.")
    exit()

if not page_names:
    print(f"No pages found in '{pages_file}'. Make sure the file is not empty.")
    exit()

print(f"Available pages for random requests: {page_names}")

# Fake User-Agent list
user_agents = [
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0"
]

while True:
    try:
        # Randomize User-Agent and page
        headers = {"User-Agent": random.choice(user_agents)}
        random_page = random.choice(page_names)
        url = f"{base_url}/{random_page}"
        
        # Make the request
        print(f"Requesting {url} with User-Agent: {headers['User-Agent']}...")
        response = requests.get(url, headers=headers)
        print(f"Response: {response.status_code}")
        
        # Randomize sleep interval using a random function
        sleep_interval = random.random() * 10  # Generates a random number between 0 and 10 seconds
        print(f"Sleeping for {sleep_interval:.2f} seconds...")
        time.sleep(sleep_interval)

    except KeyboardInterrupt:  # Quit if needed
        print("\nSimulation stopped.")
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        break
