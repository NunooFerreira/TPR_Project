import pandas as pd
from datetime import datetime, timedelta

# Define the log file and output CSV
log_file = 'logs.txt'
output_csv = 'Combined_5min_metrics.csv'

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

    df['time_diff'] = df['timestamp'].diff().dt.total_seconds().fillna(0)

    start_time = df['timestamp'].min()
    end_time = df['timestamp'].max()

    current_start = start_time
    window_size = timedelta(minutes=5)
    slide_step = timedelta(minutes=1)

    results = []

    while current_start + window_size <= end_time:
        window_data = df[(df['timestamp'] >= current_start) & (df['timestamp'] < current_start + window_size)]

        numRequests = len(window_data)
        tamanhoResposta = window_data['tamanhoResposta'].sum()
        totalImageSize = window_data.loc[window_data['is_image'], 'image_size'].sum()
        requestsJS = window_data['is_js'].sum()
        requestsHTML = window_data['is_html'].sum()
        requestsCSS = window_data['is_css'].sum()

        time_diffs = window_data['time_diff']
        avg_time_diff = time_diffs.mean() if not time_diffs.empty else 0

        time_diffs_gt_3 = time_diffs[time_diffs > 3]
        avg_time_diff_gt_3 = time_diffs_gt_3.mean() if not time_diffs_gt_3.empty else 0

        averages = {
            'avgNumRequests': numRequests / 10,  # 10 sub-windows of 30 seconds
            'avgTamanhoResposta': tamanhoResposta / 10,
            'avgTotalImageSize': totalImageSize / 10,
            'avgRequestsJS': requestsJS / 10,
            'avgRequestsHTML': requestsHTML / 10,
            'avgRequestsCSS': requestsCSS / 10
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
            'avgTimeDiff': avg_time_diff,
            'avgTimeDiffGT3': avg_time_diff_gt_3, 
            'window_start': current_start,
            'window_end': current_start + window_size
        }

        results.append(metrics)
        current_start += slide_step

    results_df = pd.DataFrame(results)
    results_df.to_csv(output_csv, index=False)
    print(f"Combined 5-minute metrics saved to {output_csv}")
