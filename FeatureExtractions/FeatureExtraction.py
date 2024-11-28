import re
import pandas as pd
from datetime import datetime, timedelta

#### 
#Final CSV Structure: #The first lines contain the global summary of means and variances. 
#The subsequent lines contain the detailed metrics for each sub-window. 
######

def process_logs(log_file, output_file, window=4, sub_window=0.5):
    # Regex for extracting information from the logs
    log_pattern = re.compile(
        r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<datetime>.*?)\] \"(?P<method>\w+) (?P<path>.*?) HTTP/.*\" \d+ (?P<size>\d+)'
    )
    metrics = []

    # Read and process log file
    with open(log_file, 'r') as f:
        for line in f:
            match = log_pattern.search(line)
            if match:
                ip = match.group('ip')
                dt_str = match.group('datetime').split()[0]
                dt = datetime.strptime(dt_str, "%d/%b/%Y:%H:%M:%S")
                method = match.group('method')
                path = match.group('path')
                size = int(match.group('size'))

                # Determine type of request for metrics (JS, HTML, CSS, Image)
                is_js = '.js' in path
                is_html = '.html' in path
                is_css = '.css' in path
                is_image = any(ext in path for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'])

                # Append the log entry to the metrics array
                metrics.append([dt, ip, method, size, is_js, is_html, is_css, is_image])

    # Convert metrics to a pandas DataFrame
    df = pd.DataFrame(metrics, columns=['datetime', 'ip', 'method', 'size', 'is_js', 'is_html', 'is_css', 'is_image'])

    # Define time windows for processing
    start_time = df['datetime'].min()
    end_time = df['datetime'].max()
    time_windows = pd.date_range(start=start_time, end=end_time, freq='4min')
    sub_windows = pd.date_range(start=start_time, end=end_time, freq=f'{int(sub_window * 60)}s')

    output_data = []
    window_counter = 1

    # Process time windows and sub-windows
    for tw_start in time_windows:
        tw_end = tw_start + timedelta(minutes=window)
        df_tw = df[(df['datetime'] >= tw_start) & (df['datetime'] < tw_end)]

        for sw_start in sub_windows[(sub_windows >= tw_start) & (sub_windows < tw_end)]:
            sw_end = sw_start + timedelta(seconds=int(sub_window * 60))
            df_sw = df_tw[(df_tw['datetime'] >= sw_start) & (df_tw['datetime'] < sw_end)]

            if not df_sw.empty:
                for ip, group in df_sw.groupby('ip'):
                    avg_file_size = group['size'].mean()  # Average size of files requested by this IP in the sub-window
                    avg_image_size = group[group['is_image']]['size'].mean() if not group[group['is_image']].empty else 0
                    output_data.append({
                        'time_window_number': window_counter,
                        'sub_window_start': sw_start,
                        'ip': ip,
                        'numRequests': len(group),
                        'tamanhoResposta': group['size'].sum(),
                        'avgFileSize': avg_file_size,
                        'avgImageSize': avg_image_size,
                        'numRequestsJS': group['is_js'].sum(),
                        'numRequestsHTML': group['is_html'].sum(),
                        'numRequestsCSS': group['is_css'].sum(),
                        'numGET': (group['method'] == 'GET').sum()
                    })

        window_counter += 1

    # Create DataFrame with sub-window data
    output_df = pd.DataFrame(output_data)

    # Calculate overall mean and variance metrics per time window
    stats_data = []
    for window_num, group in output_df.groupby('time_window_number'):
        for ip, ip_group in group.groupby('ip'):
            mean_values = ip_group[['numRequests', 'tamanhoResposta', 'avgFileSize', 'avgImageSize', 'numRequestsJS', 'numRequestsHTML', 'numRequestsCSS', 'numGET']].mean()
            variance_values = ip_group[['numRequests', 'tamanhoResposta', 'avgFileSize', 'avgImageSize', 'numRequestsJS', 'numRequestsHTML', 'numRequestsCSS', 'numGET']].var()

            stats_data.append({
                'time_window_number': window_num,
                'ip': ip,
                'mean_numRequests': mean_values['numRequests'],
                'mean_tamanhoResposta': mean_values['tamanhoResposta'],
                'mean_avgFileSize': mean_values['avgFileSize'],     #Pode nao ser preciso
                'mean_avgImageSize': mean_values['avgImageSize'],
                'mean_numRequestsJS': mean_values['numRequestsJS'],
                'mean_numRequestsHTML': mean_values['numRequestsHTML'],
                'mean_numRequestsCSS': mean_values['numRequestsCSS'],
                'mean_numGET': mean_values['numGET'],
                'variance_numRequests': variance_values['numRequests'],
                'variance_tamanhoResposta': variance_values['tamanhoResposta'],
                'variance_avgFileSize': variance_values['avgFileSize'],
                'variance_avgImageSize': variance_values['avgImageSize'],
                'variance_numRequestsJS': variance_values['numRequestsJS'],
                'variance_numRequestsHTML': variance_values['numRequestsHTML'],
                'variance_numRequestsCSS': variance_values['numRequestsCSS'],
                'variance_numGET': variance_values['numGET']     #Pode nao ser preciso
            })

    # Create stats DataFrame
    stats_df = pd.DataFrame(stats_data)

    # Calculate global averages and variances
    metric_columns = stats_df.columns.difference(['time_window_number', 'ip'])
    global_means = stats_df[metric_columns].mean(numeric_only=True)
    global_variances = stats_df[metric_columns].var(numeric_only=True)
    global_summary = {
        'metric': ['mean', 'variance'],
    }
    for col in global_means.index:
        global_summary[col] = [global_means[col], global_variances[col]]

    global_summary_df = pd.DataFrame(global_summary)

    # Save the global summary and detailed stats to CSV
    with open(f'processed_{output_file}', 'w') as f:
        global_summary_df.to_csv(f, index=False)
        stats_df.to_csv(f, index=False, mode='a')

# Run the script
process_logs('logs.txt', 'Outputmetrics.csv')
print("Ficheiro guardado no processed_Outputmetrics.csv")
