import webbrowser
import time

# Define the URL directly
while(1):

    link = "http://127.0.0.1/index.html"
    time.sleep(5)
    print(f"opening {link}")
    webbrowser.open(link)

