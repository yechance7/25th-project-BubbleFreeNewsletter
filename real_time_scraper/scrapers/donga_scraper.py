import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
import logging
import time
import os

logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

# Define a maximum number of concurrent requests
CONCURRENT_REQUESTS = 10

async def fetch(session, url, idx, semaphore):
    async with semaphore:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    news_body_tag = soup.find('section', class_='news_view')
                    img_tag = soup.find('img')  # Extract the first image tag

                    if news_body_tag:
                        news_body = news_body_tag.get_text(strip=True)
                        img_src = img_tag['src'] if img_tag else ''  # Get the image source or an empty string
                        logging.info(f"Successfully fetched data from URL: {url} (index: {idx})")
                        save_article(url, news_body, img_src)
                    else:
                        logging.warning(f"'section' with class 'news_view' not found in URL: {url} (index: {idx})")
                else:
                    logging.error(f"Failed to fetch URL: {url} with status code: {response.status} (index: {idx})")
        except aiohttp.ClientResponseError as e:
            logging.error(f"ClientResponseError for URL: {url} with status code: {e.status} (index: {idx})")
        except aiohttp.ClientError as e:
            logging.error(f"ClientError for URL: {url} with exception: {str(e)} (index: {idx})")
        except Exception as e:
            logging.error(f"An unknown error occurred for URL: {url} with exception: {str(e)} (index: {idx})")

def save_article(url, body, img_src):
    output_file = 'new_data/processed_csv/donga_article.csv'
    
    # Remove the existing file if it exists before the first write
    if not hasattr(save_article, 'file_checked'):
        if os.path.isfile(output_file):
            os.remove(output_file)
            logging.info(f"Removed existing file: {output_file}")
        save_article.file_checked = True

    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Write to CSV with headers only if the file doesn't exist
    file_exists = os.path.isfile(output_file)
    df = pd.DataFrame({
        'URL': [url],
        'Article': [body],
        'Image': [img_src]
    })
    df.to_csv(output_file, mode='a', header=not file_exists, index=False, quoting=1)  # quoting=1 to quote the Article content
    logging.info(f"Saved article to CSV: {url}")

async def main(urls):
    semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)
    async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0"}) as session:
        tasks = [fetch(session, url, idx, semaphore) for idx, url in enumerate(urls)]
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    filepath = 'new_data/raw_csv/donga.csv'
    df = pd.read_csv(filepath)
    urls = df['URL'].tolist()
    
    start_time = time.time()

    asyncio.run(main(urls))

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total elapsed time: {elapsed_time:.2f} seconds")
