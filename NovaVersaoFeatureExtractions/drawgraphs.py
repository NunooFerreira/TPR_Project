import pandas as pd
import matplotlib.pyplot as plt
import sys



#df = pd.read_csv('30s_window_metrics.csv')
# df = pd.read_csv('Count_5min__window_metrics.csv')
# df = pd.read_csv('Average_5min_avg_metrics.csv')

# ax=[]
# for i in range(6):
#     ax.append(plt.subplot(3,2,i+1))

t = df['window_start']
t = [tt[11:] for tt in t]


metrics = list(df.keys())
for i in range(6):
    fig=plt.figure(figsize=(12,5))
    ax=plt.axes()

    ax.plot(t,df[metrics[i]], linewidth=2)
    ax.set_xticks(t[0:-1:10])
    ax.set_xlabel('Time [HH:MM:SS]')
    ax.set_ylabel(metrics[i])
    fig.tight_layout(pad=0.4)
    fig.savefig(f'trafic_figures/{metrics[i]}.png',dpi=300)

plt.show()