import pandas as pd
import os

#Merges 2 CSV files and adds a Label collum with number 1 that is the anomalys, 0 is what we defined as normal data.

num_files = int(input("Enter the number of CSV files to merge: "))
if num_files <= 0:
    print("The number of files must be greater than zero.")
    exit()

# Collect file names or paths
csv_files = []
for i in range(num_files):
    file_name = input(f"Enter the full path or name of CSV file {i + 1}: ").strip()
    if not os.path.exists(file_name):
        print(f"File '{file_name}' does not exist. Please check the path and try again.")
        exit()
    csv_files.append(file_name)

processed_dataframes = []
for file in csv_files:
    df = pd.read_csv(file)

    # Remove 'window_start' and 'window_end' columns if they exist
    df = df.drop(columns=['window_start', 'window_end'], errors='ignore')

    # Add the 'Label' column with value 1
    df['Label'] = 1

    processed_dataframes.append(df)

# Merge all dataframes into one
merged_data = pd.concat(processed_dataframes, ignore_index=True)

# Ask for the output file name
output_file = input("Enter the output file name (with .csv extension): ").strip()
if not output_file.endswith('.csv'):
    print("Output file must have a .csv extension.")
    exit()

# Save the merged data to the output file
merged_data.to_csv(output_file, index=False)
print(f"Successfully merged {num_files} files into {output_file}")
