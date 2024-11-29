import pandas as pd
from datetime import datetime, timedelta

# Define the log file and output CSVs
log_file = 'logs.txt'
teste_30s_csv = '30s_window_metrics.csv'
output_5min_csv = '5min_shifted_window_metrics.csv'

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

# Process logs and calculate metrics for both 30-second and 5-minute sliding windows
def process_logs(log_file, teste_30s_csv, output_5min_csv):
    df = read_logs(log_file)
    df.sort_values(by='timestamp', inplace=True)

    start_time = df['timestamp'].min()
    end_time = df['timestamp'].max()

    current_start_30s = start_time
    window_30s_size = timedelta(seconds=30)

    current_start_5min = start_time
    window_5min_size = timedelta(minutes=5)
    slide_step = timedelta(minutes=1)

    results_30s = []
    results_5min = []

    # Calculate 30-second windows
    while current_start_30s + window_30s_size <= end_time:
        metrics = calculate_metrics(df, current_start_30s, current_start_30s + window_30s_size)
        metrics['window_start'] = current_start_30s
        metrics['window_end'] = current_start_30s + window_30s_size
        results_30s.append(metrics)
        current_start_30s += window_30s_size

    # Calculate 5-minute sliding windows
    while current_start_5min + window_5min_size <= end_time:
        metrics = calculate_metrics(df, current_start_5min, current_start_5min + window_5min_size)
        metrics['window_start'] = current_start_5min
        metrics['window_end'] = current_start_5min + window_5min_size
        results_5min.append(metrics)
        current_start_5min += slide_step

    # Save results to CSVs
    results_30s_df = pd.DataFrame(results_30s)
    results_30s_df.to_csv(teste_30s_csv, index=False)

    results_5min_df = pd.DataFrame(results_5min)
    results_5min_df.to_csv(output_5min_csv, index=False)

# Run the script
if __name__ == "__main__":
    process_logs(log_file, teste_30s_csv, output_5min_csv)
    print(f"30-second window metrics saved to {teste_30s_csv}")
    print(f"5-minute sliding window metrics saved to {output_5min_csv}")
