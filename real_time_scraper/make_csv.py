import pandas as pd
import os
from datetime import datetime, timedelta

# Define the directory containing the Excel files
current_dir = os.getcwd()
new_data_dir = os.path.join(current_dir, 'new_data')
csv_dir = os.path.join(new_data_dir, 'raw_csv')

# Create the csv directory if it doesn't exist
if not os.path.exists(csv_dir):
    os.makedirs(csv_dir)

# Get today's date in the format YYYYMMDD
today = datetime.today().strftime('%Y%m%d')
yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y%m%d')

# Construct the expected filename based on yesterday's and today's dates
expected_filename = f'NewsResult_{yesterday}-{today}.xlsx'

# Full path to the expected Excel file
excel_path = os.path.join(new_data_dir, expected_filename)

# Mapping of 언론사 to CSV file names
media_to_csv = {
    "중앙일보": "joongang.csv",
    "조선일보": "chosun.csv",
    "경향신문": "khan.csv",
    "한겨레": "hani.csv",
    "동아일보": "donga.csv"
}

# Check if the file exists
if os.path.exists(excel_path):
    # Read the Excel file
    df = pd.read_excel(excel_path)
    
    # Group by the '언론사' column
    grouped = df.groupby('언론사')

    # Iterate through the groups and save each to a corresponding CSV file
    for name, group in grouped:
        if name in media_to_csv:
            # Define the output CSV file path
            output_csv = os.path.join(csv_dir, media_to_csv[name])
            
            # Remove the existing file if it exists
            if os.path.exists(output_csv):
                os.remove(output_csv)
                print(f"Removed existing file: {output_csv}")
            
            # Save the group to a CSV file
            group.to_csv(output_csv, index=False)
            print(f"Saved group '{name}' to {output_csv}")
        else:
            print(f"Unknown 언론사: {name}")
else:
    print(f"No file found with the name {expected_filename} in the directory {new_data_dir}.")
