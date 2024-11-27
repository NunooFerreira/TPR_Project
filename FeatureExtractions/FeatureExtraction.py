import re
import pandas as pd
from datetime import datetime, timedelta

# Função para processar e extrair as métricas dos logs
def process_logs(log_file, output_file, window=4, sub_window=0.5):
    # Regex para extrair informações do log
    log_pattern = re.compile(
        r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<datetime>.*?)\] "(?P<method>\w+) (?P<path>.*?) HTTP/.*" \d+ (?P<size>\d+)'
    )
    metrics = []

    # Leitura e processamento do ficheiro dos logs
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

                # Definir tipo de request para métricas (Extrair o tipo de extensoes que queremos apartir do grupo Path)
                is_js = '.js' in path
                is_html = '.html' in path
                is_css = '.css' in path

                # Adicionar a entrada de log ao array de métricas
                metrics.append([dt, ip, method, size, is_js, is_html, is_css])

    # Converter as métricas num DataFrame pandas para o processamento
    df = pd.DataFrame(metrics, columns=['datetime', 'ip', 'method', 'size', 'is_js', 'is_html', 'is_css'])

    # Definir intervalos de tempo para janelas de 5 minutos e sub-janelas de 30 segundos que definimos anteriormente.
    start_time = df['datetime'].min()
    end_time = df['datetime'].max()
    time_windows = pd.date_range(start=start_time, end=end_time, freq='4min')  # Shift windows a cada 4 minutes (podemos mudar aqui)
    sub_windows = pd.date_range(start=start_time, end=end_time, freq=f'{int(sub_window * 60)}s')

    output_data = []
    window_counter = 1  # Contador para as janelas de tempo (Aqui pode bugar o numero de janelas porque os logs ainda nao estao por ordem)

    # Process time windows and sub-windows
    for tw_start in time_windows:
        tw_end = tw_start + timedelta(minutes=window)
        df_tw = df[(df['datetime'] >= tw_start) & (df['datetime'] < tw_end)]

        for sw_start in sub_windows[(sub_windows >= tw_start) & (sub_windows < tw_end)]:
            sw_end = sw_start + timedelta(seconds=int(sub_window * 60))
            df_sw = df_tw[(df_tw['datetime'] >= sw_start) & (df_tw['datetime'] < sw_end)]

            if not df_sw.empty:
                for ip, group in df_sw.groupby('ip'):
                    output_data.append({
                        'time_window_number': window_counter,
                        'sub_window_start': sw_start,
                        'ip': ip,
                        'numRequests': len(group),  # Numero de requets feitos por um Ip
                        'tamanhoResposta': group['size'].sum(),  #Tamanho em bytes do requested
                        'numRequestsJS': group['is_js'].sum(),
                        'numRequestsHTML': group['is_html'].sum(),
                        'numRequestsCSS': group['is_css'].sum(),
                        'numGET': (group['method'] == 'GET').sum()  #Isto neste momento é o mesmo que numReq caso so tenhamos GET's
                    })

        window_counter += 1 # Incrementar o número da janela de tempo

    # Criar DataFrame com os dados dos subjanela
    output_df = pd.DataFrame(output_data)

    # Agora calculamos as estatísticas (média, variância) por IP para cada janela de 5 minutos
    stats_data = []
    for window_num, group in output_df.groupby('time_window_number'):
        for ip, ip_group in group.groupby('ip'):
            mean_values = ip_group[['numRequests', 'tamanhoResposta', 'numRequestsJS', 'numRequestsHTML', 'numRequestsCSS', 'numGET']].mean()
            variance_values = ip_group[['numRequests', 'tamanhoResposta', 'numRequestsJS', 'numRequestsHTML', 'numRequestsCSS', 'numGET']].var()

            stats_data.append({
                'time_window_number': window_num,
                'ip': ip,
                'mean_numRequests': mean_values['numRequests'],
                'mean_tamanhoResposta': mean_values['tamanhoResposta'],
                'mean_numRequestsJS': mean_values['numRequestsJS'],
                'mean_numRequestsHTML': mean_values['numRequestsHTML'],
                'mean_numRequestsCSS': mean_values['numRequestsCSS'],
                'mean_numGET': mean_values['numGET'],
                'variance_numRequests': variance_values['numRequests'],
                'variance_tamanhoResposta': variance_values['tamanhoResposta'],
                'variance_numRequestsJS': variance_values['numRequestsJS'],
                'variance_numRequestsHTML': variance_values['numRequestsHTML'],
                'variance_numRequestsCSS': variance_values['numRequestsCSS'],
                'variance_numGET': variance_values['numGET'],
                #Covariancia nao e preciso, o ML faz isso
            })


    # Criar DataFrame e salvar no CSV
    stats_df = pd.DataFrame(stats_data)
    stats_df.to_csv(f'processed_{output_file}', index=False)

# Executar o script
process_logs('logs.txt', 'Outputmetrics.csv')
print("Ficheiro guardado no processed_Outputmetrics.csv")
