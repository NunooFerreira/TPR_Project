import pandas as pd
import os

def merge_csv_files():
    """
    Merges a specified number of CSV files provided by the user into a single CSV file.
    """
    try:
        # Ask for the number of files to merge
        num_files = int(input("Enter the number of CSV files to merge: "))
        if num_files <= 0:
            print("The number of files must be greater than zero.")
            return

        # Collect file names or paths
        csv_files = []
        for i in range(num_files):
            file_name = input(f"Enter the full path or name of CSV file {i + 1}: ").strip()
            if not os.path.exists(file_name):
                print(f"File '{file_name}' does not exist. Please check the path and try again.")
                return
            csv_files.append(file_name)
        
        # Read and concatenate all specified CSV files
        merged_data = pd.concat([pd.read_csv(file) for file in csv_files])
        
        # Ask for the output file name
        output_file = input("Enter the output file name (with .csv extension): ").strip()
        if not output_file.endswith('.csv'):
            print("Output file must have a .csv extension.")
            return
        
        # Save the merged data to the output file
        merged_data.to_csv(output_file, index=False)
        print(f"Successfully merged {num_files} files into {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the script
merge_csv_files()
