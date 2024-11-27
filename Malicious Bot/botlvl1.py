import time
import requests

# File containing the list of HTML pages
pages_file = "resources/htmlpages.txt"

# Base URL of the website (Apache server running locally)
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

# Choose the first page to request
page_to_request = page_names[0]
print(f"Simulating requests for: {page_to_request}")

while True:
    try:
        url = f"{base_url}/{page_to_request}"
        print(f"Requesting {url}...")
        response = requests.get(url)
        print(f"Response: {response.status_code}")
        time.sleep(2)  # Wait for 2 seconds before the next request
    except KeyboardInterrupt:
        print("\nSimulation stopped.")
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        break
