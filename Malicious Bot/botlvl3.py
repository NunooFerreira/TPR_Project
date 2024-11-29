import time
import requests
import random

#Repeatedly request a random page every "x" seconds (using sleep(x))

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

# Set the interval between requests (in seconds)
request_interval = 2  # Change this value for different sleep intervals



while True:
    try:
        #Usar um Fake User-Agent randomly
        user_agents = [
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0",
        ]
        headers = {"User-Agent": random.choice(user_agents)}
        
        # Select a random page
        random_page = random.choice(page_names)
        url = f"{base_url}/{random_page}"
        print(f"Requesting {url}...")
        response = requests.get(url, headers=headers)  #Adicionar ou Remover o headers=headers, para remover o fake agent.
        print(f"Response: {response.status_code}")
        time.sleep(request_interval)  # Wait for the interval before the next request
    except KeyboardInterrupt:  # Quit if needed
        print("\nSimulation stopped.")
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        break
