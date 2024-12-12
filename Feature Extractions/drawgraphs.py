import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('Bot_Combined_5min_metrics.csv')                 #Mudar o ficheiro para dar plot
# df = pd.read_csv('Count_5min__window_metrics.csv')
# df = pd.read_csv('Average_5min_avg_metrics.csv')

t = df['window_start']
t = [tt[11:] for tt in t]   #queremos apartir da coluna 11, das horas

metrics = list(df.keys())

for i in range(0,14):       #6 a 12 para ir da columa 7-12 com os averages, ou range(6) para fazer as 6 primeiras colunas
    fig=plt.figure(figsize=(12,5))
    ax=plt.axes()

    ax.plot(t,df[metrics[i]], linewidth=2)
    ax.set_xticks(t[0:-1:10])
    ax.set_xlabel('Time [HH:MM:SS]')
    ax.set_ylabel(metrics[i])
    fig.tight_layout(pad=0.4)
    fig.savefig(f'trafic_figures/{metrics[i]}.png',dpi=300)

plt.show()