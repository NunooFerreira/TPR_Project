import time
import subprocess

url = "http://127.0.0.1"
sleep_time = 5  # Adjust as needed

while True:
    subprocess.run(["curl", "-s", url])
    time.sleep(sleep_time)
