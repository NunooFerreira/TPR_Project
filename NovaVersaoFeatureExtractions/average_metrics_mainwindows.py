import pandas as pd
from datetime import datetime, timedelta

# Define the log file and output CSV
log_file = 'logs.txt'
output_avg_csv = '5min_avg_metrics.csv'

# Function to parse log lines
def parse_log_line(line):
    parts = line.split()
    if len(parts) < 9:
        return None

    try:
        ip = parts[0]
        timestamp = datetime.strptime(parts[3][1:], "%d/%b/%Y:%H:%M:%S")
        url = parts[6]

        is_js = url.endswith('.js')
        is_html = url.endswith('.html')
        is_css = url.endswith('.css')
        is_image = url.endswith(('.png', '.jpg', '.jpeg', '.gif', '.ico'))

        tamanhoResposta = int(parts[9]) if len(parts) > 9 and parts[9].isdigit() else 0

        image_size = tamanhoResposta if is_image else 0

        return {
            'ip': ip,
            'timestamp': timestamp,
            'tamanhoResposta': tamanhoResposta,
            'is_js': is_js,
            'is_html': is_html,
            'is_css': is_css,
            'is_image': is_image,
            'image_size': image_size
        }
    except Exception as e:
        return None

# Read and parse the log file
def read_logs(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            parsed = parse_log_line(line)
            if parsed:
                data.append(parsed)
    return pd.DataFrame(data)

# Calculate metrics within a time window
def calculate_metrics(df, start_time, end_time):
    window_data = df[(df['timestamp'] >= start_time) & (df['timestamp'] < end_time)]
    metrics = {
        'numRequests': len(window_data),
        'tamanhoResposta': window_data['tamanhoResposta'].sum(),
        'totalImageSize': window_data.loc[window_data['is_image'], 'image_size'].sum(),
        'RequestsJS': window_data['is_js'].sum(),
        'RequestsHTML': window_data['is_html'].sum(),
        'RequestsCSS': window_data['is_css'].sum()
    }
    return metrics

# Process logs and calculate average metrics for 5-minute sliding windows
def process_logs(log_file, output_avg_csv):
    df = read_logs(log_file)
    df.sort_values(by='timestamp', inplace=True)

    start_time = df['timestamp'].min()
    end_time = df['timestamp'].max()

    current_start = start_time
    window_size = timedelta(minutes=5)
    slide_step = timedelta(minutes=1)

    results = []

    # Calculate averages for each 5-minute sliding window
    while current_start + window_size <= end_time:
        metrics = calculate_metrics(df, current_start, current_start + window_size)
        averages = {
            'avgNumRequests': metrics['numRequests'] / 10,  # 10 sub-windows of 30 seconds
            'avgTamanhoResposta': metrics['tamanhoResposta'] / 300,  # 300 seconds
            'avgTotalImageSize': metrics['totalImageSize'] / 300,
            'avgRequestsJS': metrics['RequestsJS'] / 10,
            'avgRequestsHTML': metrics['RequestsHTML'] / 10,
            'avgRequestsCSS': metrics['RequestsCSS'] / 10,
            'window_start': current_start,
            'window_end': current_start + window_size
        }
        results.append(averages)
        current_start += slide_step

    # Save results to CSV
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_avg_csv, index=False)

# Run the script
if __name__ == "__main__":
    process_logs(log_file, output_avg_csv)
    print(f"5-minute average metrics saved to {output_avg_csv}")
