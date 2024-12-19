import pandas as pd
import matplotlib.pyplot as plt

def plot_metrics(normal_csv, bot_csv, column):

    normal_data = pd.read_csv("../OutputedCsv/Nuno_Combined_5min_metrics.csv")
    bot_data = pd.read_csv("../OutputedCsv/WithWiondows_BOTLVL8_Combined_5min_metrics.csv")

    # Ensure the column exists
    if column not in normal_data.columns or column not in bot_data.columns:
        print(f"Column '{column}' not found in one or both CSVs.")
        return

    # Limit data to 1 hour (12 entries assuming 5-minute windows)
    normal_data = normal_data.head(57)
    bot_data = bot_data.head(57)


    # Calculate variance and rolling averages
    normal_variance = normal_data[column].rolling(window=5, min_periods=1).var()
    bot_variance = bot_data[column].rolling(window=5, min_periods=1).var()

    # Direct averages for each window
    normal_average = normal_data[column]
    bot_average = bot_data[column]

    # Plot variance
    plt.figure(figsize=(10, 6))
    plt.plot(normal_variance, label='Normal User Variance', color='blue', alpha=0.7)
    plt.plot(bot_variance, label='Bot Variance', color='red', alpha=0.7)
    plt.title(f'Comparison of Variance for {column}')
    plt.xlabel('Time (5-minute windows)')
    plt.ylabel('Variance')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Plot direct averages
    plt.figure(figsize=(10, 6))
    plt.plot(normal_average, label='Normal User Average', color='blue', alpha=0.7)
    plt.plot(bot_average, label='Bot Average', color='red', alpha=0.7)
    plt.title(f'Comparison of Averages for {column}')
    plt.xlabel('Time (5-minute windows)')
    plt.ylabel('Average Value')
    plt.legend()
    plt.grid(True)
    plt.show()

# Example usage
normal_csv = "normal_user.csv"
bot_csv = "bot.csv"
column = "numRequests"  # Replace with your chosen column

plot_metrics(normal_csv, bot_csv, column)
