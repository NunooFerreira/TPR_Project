import pandas as pd
import matplotlib.pyplot as plt


#Script para dar Graficos 2d:

normal_csv = pd.read_csv("../OutputedCsv/Nuno_Combined_5min_metrics.csv")
bot_csv = pd.read_csv("../OutputedCsv/BOTLVL8_Combined_5min_metrics.csv")

#downsampled_normal = normal_csv['avgSilenceTime'].iloc[::2].reset_index(drop=True)  # Take every other data point (or more sophisticated methods)

# Printing values of the points
#print("Normal Users (Rescaled) Data Points:")
#print(downsampled_normal)

#print("\nBot Level1 Data Points:")
#print(bot_csv['numRequests'])
plt.figure(figsize=(12, 6))

# Plot the normal data (after downsampling) with blue color
plt.plot(normal_csv['avgNumRequests'], label="Normal Users (Rescaled)", color="blue", marker='o', linestyle='-', markersize=5)

# Plot the bot data (assumed to be in the 'numRequests' column)
plt.plot(bot_csv['avgNumRequests'], label="Bot Level8 Data", color="red", marker='s', linestyle='--', markersize=5)

# Add titles, labels, and grid
plt.title("Comparison of Normal Users vs Bot Level8 Data")
plt.xlabel("Time (Minutes)")
plt.ylabel("Average numRequests")
plt.legend()
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()
