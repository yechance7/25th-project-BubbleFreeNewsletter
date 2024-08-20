#!/bin/bash

# Run rt_main.py
echo "Running rt_main.py...Crawling..."
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

#scraping
echo "Running chosun_scraper.py"
python3 scrapers/chosun_scraper.py
if [ $? -ne 0 ]; then
    echo "Error: chosun_scraper.py failed."
    exit 1
fi

echo "Running donga_scraper.py"
python3 scrapers/donga_scraper.py
if [ $? -ne 0 ]; then
    echo "Error: donga_scraper.py failed."
    exit 1
fi

echo "Running hani_scraper.py"
python3 scrapers/hani_scraper.py
if [ $? -ne 0 ]; then
    echo "Error: hani_scraper.py failed."
    exit 1
fi

echo "Running joongang_scraper.py"
python3 scrapers/joongang_scraper.py
if [ $? -ne 0 ]; then
    echo "Error: joongang_scraper.py failed."
    exit 1
fi

echo "Running khan_scraper.py"
python3 scrapers/khan_scraper.py
if [ $? -ne 0 ]; then
    echo "Error: khan_scraper.py failed."
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
