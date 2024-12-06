import webbrowser
import time
import random

urls = [
    "blog.html",
    "about.html",
    "index.html",
    "career.html"
]

while True:
    # Select a random page from the list
    selected_page = random.choice(urls)

    # Construct the full URL
    full_url = "http://127.0.0.1/" + selected_page

    # Visit the constructed URL
    print(f"Opening {full_url}")
    webbrowser.open(full_url)
    time.sleep(5)