import time
import requests
import random

#Repeatedly request a random page every random seconds using gaucian (using random agents)

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

print(f"Available pages for Gaussian random requests: {page_names}")

# Fake User-Agent list
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0",
    "Safari/537.36 (iPhone; CPU iPhone OS 15_0 like Mac OS X)"
]

# Gaussian distribution parameters (Escolher aqui os valores de acordo com a media do numero de vezes que clicamos no website.)
mean_sleep = 5  # Mean sleep interval in seconds   
std_dev_sleep = 2  # Standard deviation of sleep interval

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
        
        # Generate Gaussian random sleep interval
        sleep_interval = max(0, random.gauss(mean_sleep, std_dev_sleep))  # Ensure non-negative sleep
        print(f"Sleeping for {sleep_interval:.2f} seconds...")
        time.sleep(sleep_interval)
    except KeyboardInterrupt:  # Quit if needed
        print("\nSimulation stopped.")
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        break
