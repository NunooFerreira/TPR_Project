import time
import requests

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

# Select 4 fixed pages from the file (or fewer if there are less than 4 pages in the file)
pages_to_request = page_names[:4]  # First 4 pages in the list
if len(pages_to_request) < 4:
    print(f"Warning: Only {len(pages_to_request)} pages found. Using all available pages.")

print(f"Simulating requests for these pages: {pages_to_request}")

# Set the interval between requests (in seconds)
request_interval = 2  # Change this value for different sleep intervals

while True:
    try:
        for page in pages_to_request:
            url = f"{base_url}/{page}"
            print(f"Requesting {url}...")
            response = requests.get(url)
            print(f"Response: {response.status_code}")
            time.sleep(request_interval)  # Wait for the interval before requesting the next page
    except KeyboardInterrupt:  # Quit if needed
        print("\nSimulation stopped.")
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        break
