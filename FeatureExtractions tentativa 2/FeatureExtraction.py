import re
from datetime import datetime
from collections import defaultdict
import csv

# Padrão regex para extrair informações de cada linha do log
log_pattern = r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(.*?)" (\d{3}) (\d+) "(.*?)" "(.*?)"'

# Função para extrair dados dos logs e calcular features
def extract_features(log_file):
    features = {
        "requests_per_ip": defaultdict(int),
        "uris_per_ip": defaultdict(lambda: defaultdict(int)),
        "status_codes": defaultdict(int),
        "bytes_per_ip": defaultdict(int),
        "user_agents": defaultdict(set),
        "request_intervals": defaultdict(list)
    }
    last_request_time = {}

    # Abrir o arquivo de logs e processar linha a linha
    with open(log_file, 'r') as file:
        for line in file:
            match = re.search(log_pattern, line)
            if match:
                ip, timestamp, request, status, size, referer, user_agent = match.groups()
                uri = request.split()[1] if " " in request else "/"
                timestamp = datetime.strptime(timestamp, "%d/%b/%Y:%H:%M:%S %z")

                # Feature 1: Contagem de requisições por IP
                features["requests_per_ip"][ip] += 1

                # Feature 2: Distribuição de URIs por IP
                features["uris_per_ip"][ip][uri] += 1

                # Feature 3: Contagem de códigos de status HTTP
                features["status_codes"][status] += 1

                # Feature 4: Total de bytes transferidos por IP
                features["bytes_per_ip"][ip] += int(size)

                # Feature 5: Armazena o User-Agent por IP
                features["user_agents"][ip].add(user_agent)

                # Feature 6: Intervalo entre requisições do mesmo IP
                if ip in last_request_time:
                    interval = (timestamp - last_request_time[ip]).total_seconds()
                    features["request_intervals"][ip].append(interval)
                last_request_time[ip] = timestamp

    # Pós-processamento: média do intervalo entre requisições por IP
    for ip, intervals in features["request_intervals"].items():
        if intervals:
            features["request_intervals"][ip] = sum(intervals) / len(intervals)
        else:
            features["request_intervals"][ip] = None

    return features

# Função para salvar as features extraídas em um arquivo CSV
def save_features_to_csv(features, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Cabeçalho do CSV
        writer.writerow(["Feature", "IP", "Value"])

        # Salvar `requests_per_ip`
        for ip, count in features["requests_per_ip"].items():
            writer.writerow(["requests_per_ip", ip, count])

        # Salvar `uris_per_ip`
        for ip, uris in features["uris_per_ip"].items():
            for uri, count in uris.items():
                writer.writerow(["uris_per_ip", f"{ip} -> {uri}", count])

        # Salvar `status_codes`
        for status_code, count in features["status_codes"].items():
            writer.writerow(["status_codes", status_code, count])

        # Salvar `bytes_per_ip`
        for ip, byte_count in features["bytes_per_ip"].items():
            writer.writerow(["bytes_per_ip", ip, byte_count])

        # Salvar `user_agents`
        for ip, user_agents in features["user_agents"].items():
            writer.writerow(["user_agents", ip, "; ".join(user_agents)])

        # Salvar `request_intervals`
        for ip, interval_avg in features["request_intervals"].items():
            writer.writerow(["request_intervals", ip, interval_avg])

# Exemplo de uso
log_file = 'extractionlogs.txt'
output_file = 'outExtractedFeatures.csv'

# Extração das features e salvamento no arquivo CSV
features = extract_features(log_file)
save_features_to_csv(features, output_file)

print(f"Features extraídas foram salvas no arquivo {output_file}")
