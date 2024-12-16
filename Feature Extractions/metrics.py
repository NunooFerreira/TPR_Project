import pandas as pd
from datetime import datetime, timedelta

# Define the log file and output CSV
log_file = '../AccessLogs/botlvl5.log'
output_csv = '../OutputedCsv/BOTLVL5_Combined_5min_metrics.csv'

#ULTIMAS DUAS LINHAS SAO O MAX E MIN RESPETIVAMENTE.

data = []

# Read and parse log file
with open(log_file, 'r') as f:
    for line in f:
        parts = line.split()
        if len(parts) < 9:
            continue

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

            data.append({
                'ip': ip,
                'timestamp': timestamp,
                'tamanhoResposta': tamanhoResposta,
                'is_js': is_js,
                'is_html': is_html,
                'is_css': is_css,
                'is_image': is_image,
                'image_size': image_size
            })

        except Exception as e:
            continue

    df = pd.DataFrame(data)
    df.sort_values(by='timestamp', inplace=True)

    start_time = df['timestamp'].min()
    end_time = df['timestamp'].max()

    current_start = start_time
    window_size = timedelta(minutes=5)
    slide_step = timedelta(minutes=1)

    results = []

    while current_start + window_size <= end_time:
        window_data = df[(df['timestamp'] >= current_start) & (df['timestamp'] < current_start + window_size)]

        # Silence calculation
        silence_times = []
        silence_count = 0
        total_silence_time = timedelta()

        # Group by IP and calculate silence periods
        for ip, group in window_data.groupby('ip'):
            group_sorted = group.sort_values('timestamp')
            last_request_time = None

            for _, row in group_sorted.iterrows():
                if last_request_time:
                    silence = row['timestamp'] - last_request_time
                    if silence > timedelta(seconds=1):
                        silence_times.append(silence.total_seconds())
                        total_silence_time += silence
                        silence_count += 1
                last_request_time = row['timestamp']

        numRequests = len(window_data)
        tamanhoResposta = window_data['tamanhoResposta'].sum()
        totalImageSize = window_data.loc[window_data['is_image'], 'image_size'].sum()
        requestsJS = window_data['is_js'].sum()
        requestsHTML = window_data['is_html'].sum()
        requestsCSS = window_data['is_css'].sum()

        averages = {
            'avgNumRequests': numRequests / 10,  # 10 sub-windows of 30 seconds
            'avgTamanhoResposta': tamanhoResposta / 10,
            'avgTotalImageSize': totalImageSize / 10,
            'avgRequestsJS': requestsJS / 10,
            'avgRequestsHTML': requestsHTML / 10,
            'avgRequestsCSS': requestsCSS / 10,
            'avgSilenceTime': total_silence_time.total_seconds() / (silence_count if silence_count else 1)  # Avoid division by zero
        }

        metrics = {
            'numRequests': numRequests,
            'tamanhoResposta': tamanhoResposta,
            'totalImageSize': totalImageSize,
            'RequestsJS': requestsJS,
            'RequestsHTML': requestsHTML,
            'RequestsCSS': requestsCSS,
            'avgNumRequests': averages['avgNumRequests'],
            'avgTamanhoResposta': averages['avgTamanhoResposta'],
            'avgTotalImageSize': averages['avgTotalImageSize'],
            'avgRequestsJS': averages['avgRequestsJS'],
            'avgRequestsHTML': averages['avgRequestsHTML'],
            'avgRequestsCSS': averages['avgRequestsCSS'],
            'totalSilenceTime': total_silence_time.total_seconds(),
            'avgSilenceTime': averages['avgSilenceTime'],
            'silenceCount': silence_count,
            'window_start': current_start,
            'window_end': current_start + window_size
        }

        results.append(metrics)
        current_start += slide_step

    results_df = pd.DataFrame(results)
    results_df = results_df.drop(columns=['window_start', 'window_end'])

    # # Add a row for the maximum and minimum across all columns
    # max_row = results_df.max().rename('Maximum')
    # min_row = results_df.min().rename('Minimum')
    # results_df = pd.concat([results_df, max_row.to_frame().T, min_row.to_frame().T])

    # Save to CSV
    results_df.to_csv(output_csv, index=False)
    print(f"Combined 5-minute metrics with statistics saved to {output_csv}")
