import time
import random
import subprocess

urls = [
    "http://example.com/page1",
    "http://example.com/page2",
    "http://example.com/page3",
    "http://example.com/page4"
]
sleep_time = 5  # Adjust as needed

while True:
    url = random.choice(urls)
    subprocess.run(["curl", "-s", url])
    time.sleep(sleep_time)
