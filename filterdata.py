import re
from datetime import datetime
import pandas as pd

# Define the log pattern Regular expression para dos logs:
log_pattern = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+)\s-\s-\s\[(?P<date_time>[^\]]+)\]\s"(?P<http_method>\S+)\s(?P<url>[^\s]+)\s(?P<http_version>HTTP/\d\.\d)?"\s(?P<status_code>\d+)\s(?P<response_size>\d+)\s"(?P<referrer>[^"]*)"\s"(?P<user_agent>[^"]*)"'
)

#Parse log entries
def parse_log(log_file):
    log_entries = []
    with open(log_file, 'r') as file:
        for line in file:
            match = log_pattern.search(line)
            if match:
                entry = match.groupdict()
                # Convert date_time string to a timezone-unaware datetime object
                entry['date_time'] = datetime.strptime(entry['date_time'], "%d/%b/%Y:%H:%M:%S %z").replace(tzinfo=None)
                # Append to list of log entries
                log_entries.append(entry)
    return log_entries

# Function to save parsed log entries to an Excel file
def save_to_excel(log_entries, output_file):
    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(log_entries)
    # Save the DataFrame to an Excel file
    df.to_excel(output_file, index=False)


log_file = 'logs.txt'  
parsed_logs = parse_log(log_file)

#Salvar num Exel file   
output_file = 'parsed_logs.xlsx'
save_to_excel(parsed_logs, output_file)
print("File written to an excel file")