import time
import requests

#Repeatedly request the same page every "x" seconds (using sleep(x))

# File containing the list of HTML pages, Queremos aqui JS e CSS e IMAGES Tbm
pages_file = "resources/htmlpages.txt"

# URL website (Apache server running locally)
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

# Primeiro teste com um Super Dummy Bot, Pedir apenas 1 pagina de x em x segundos estaticos... 
page_to_request = page_names[1] # Neste caso pagina 1 dos resources.
print(f"Simulating requests for the page: {page_to_request}")

#Usar um Fake User-Agent
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0"
}

while True:
    try:
        url = f"{base_url}/{page_to_request}"
        print(f"Requesting {url}...")
        response = requests.get(url, headers=headers)  #Adicionar ou Remover o headers=headers, para remover o fake agent.
        print(f"Response: {response.status_code}")
        time.sleep(2)  # Wait for 2 seconds before the next request
    except KeyboardInterrupt:   #Quit if needed
        print("\nSimulation stopped.")
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        break
