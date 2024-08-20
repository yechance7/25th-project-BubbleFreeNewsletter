import pandas as pd
import os
from datetime import datetime, timedelta

# Define the directory containing the Excel files
current_dir = os.getcwd()
new_data_dir = os.path.join(current_dir, 'new_data')

# Get today's date in the format YYYYMMDD
today = datetime.today().strftime('%Y%m%d')
yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y%m%d')

# Construct the expected filename based on yesterday's and today's dates
expected_filename = f'NewsResult_{yesterday}-{today}.xlsx'

# Full path to the expected Excel file
excel_path = os.path.join(new_data_dir, expected_filename)

# Check if the file exists
if os.path.exists(excel_path):
    # Read the Excel file
    df = pd.read_excel(excel_path)
    
    # Define the output CSV file path
    output_csv = os.path.join(new_data_dir, f'{expected_filename.replace(".xlsx", ".csv")}')
    
    # Save the entire DataFrame to a CSV file
    df.to_csv(output_csv, index=False)
    print(f"Saved the entire dataset to {os.path.basename(output_csv)}")
else:
    print(f"No file found with the name {expected_filename} in the directory {new_data_dir}.")
