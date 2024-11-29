import pandas as pd
from datetime import datetime, timedelta

# Define the log file and output CSV
log_file = 'logs.txt'
output_csv = 'TRUE_VERSION_30s_window_metrics.csv'

# Function to parse log lines
def parse_log_line(line):
    parts = line.split()
    if len(parts) < 9:
        return None

    try:
        ip = parts[0]
        timestamp = datetime.strptime(parts[3][1:], "%d/%b/%Y:%H:%M:%S")
        request = parts[5][1:]
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

# Calculate metrics within a 30-second window
def calculate_metrics(df, start_time, end_time):
    window_data = df[(df['timestamp'] >= start_time) & (df['timestamp'] < end_time)]
    metrics = {
        'numRequests': len(window_data),                    # len -> Conta o número de linhas no DataFrame filtrado para a janela.
        'tamanhoResposta': window_data['tamanhoResposta'].sum(),
        'totalImageSize': window_data.loc[window_data['is_image'], 'image_size'].sum(),
        'RequestsJS': window_data['is_js'].sum(),
        'RequestsHTML': window_data['is_html'].sum(),
        'RequestsCSS': window_data['is_css'].sum()
    }
    return metrics

# Main function to process logs and calculate 30-second windows
def process_logs(log_file, output_csv):
    df = read_logs(log_file)
    df.sort_values(by='timestamp', inplace=True)

    start_time = df['timestamp'].min()
    end_time = df['timestamp'].max()

    current_start = start_time
    window_size = timedelta(seconds=30)

    results = []

    while current_start + window_size <= end_time:
        metrics = calculate_metrics(df, current_start, current_start + window_size)
        metrics['window_start'] = current_start
        metrics['window_end'] = current_start + window_size
        results.append(metrics)
        current_start += window_size

    # Save results to CSV
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_csv, index=False)

# Run the script
if __name__ == "__main__":
    process_logs(log_file, output_csv)
    print(f"30-second window metrics saved to {output_csv}")
