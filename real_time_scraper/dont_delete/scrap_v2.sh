#!/bin/bash

# Run rt_main.py
echo "Running rt_main.py..."
python3 rt_main.py
if [ $? -ne 0 ]; then
    echo "Error: rt_main.py failed."
    exit 1
fi

# Run make_csv.py
echo "Running make_csv.py..."
python3 make_csv.py
if [ $? -ne 0 ]; then
    echo "Error: make_csv.py failed."
    exit 1
fi

# Run make_json.py
echo "Running make_json.py..."
python3 make_json.py
if [ $? -ne 0 ]; then
    echo "Error: make_json.py failed."
    exit 1
fi

# Run db_upload.py
echo "Running db_upload.py..."
python3 db_upload.py
if [ $? -ne 0 ]; then
    echo "Error: db_upload.py failed."
    exit 1
fi

echo "All scripts ran successfully."
