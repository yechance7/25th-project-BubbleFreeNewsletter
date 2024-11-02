import pandas as pd
import os
import json
from datetime import datetime, timedelta

# Define the directory containing the CSV file
current_dir = os.getcwd()
new_data_dir = os.path.join(current_dir, 'new_data')

# Get today's date in the format YYYYMMDD
today = datetime.today().strftime('%Y%m%d')
yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y%m%d')

# Construct the expected CSV filename based on yesterday's and today's dates
expected_filename = f'NewsResult_{yesterday}-{today}.csv'

# Full path to the expected CSV file
csv_path = os.path.join(new_data_dir, expected_filename)

# Mapping of 언론사 to JSON file names
media_to_json = {
    "중앙일보": "joongang.json",
    "조선일보": "chosun.json",
    "경향신문": "khan.json",
    "한겨레": "hani.json",
    "동아일보": "donga.json"
}

# Check if the file exists
if os.path.exists(csv_path):
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Replace NaN/None values with an empty string
    df = df.fillna("")
    
    # Group the DataFrame by "언론사"
    grouped = df.groupby('언론사')
    
    # Iterate through the groups and save each group to a corresponding JSON file
    for media, group in grouped:
        if media in media_to_json:
            # Convert the group to a list of dictionaries
            data = group.to_dict(orient='records')
            
            # Add the "Article" entry to each dictionary
            for item in data:
                item["Article"] = ""
            
            # Define the output JSON file path
            json_output_path = os.path.join(new_data_dir, media_to_json[media])
            
            # Save the group as a JSON file
            with open(json_output_path, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
            
            print(f"Saved data for {media} to {os.path.basename(json_output_path)}")
        else:
            print(f"Unknown 언론사: {media}")
else:
    print(f"No file found with the name {expected_filename} in the directory {new_data_dir}.")
