import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
import logging
import time


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
                    if news_body_tag:
                        news_body = news_body_tag.get_text(strip=True)
                        logging.info(f"Successfully fetched data from URL: {url} (index: {idx})")
                        save_article(url, news_body)
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

def save_article(url, body):
    df = pd.DataFrame({
        'URL': [url],
        'Body': [body],
        'Label': [0]
    })
    df.to_csv('donga_crawling.csv', mode='a', header=False, index=False)
    logging.info(f"Saved article to CSV: {url}")

async def main(urls):
    semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)
    async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0"}) as session:
        tasks = [fetch(session, url, idx, semaphore) for idx, url in enumerate(urls)]
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    filepath = '25th-project-BubbleFreeNewsletter/donga_19900101-20240808.xlsx'
    df = pd.read_excel(filepath, sheet_name='sheet', usecols=['URL'])
    urls = df['URL'].tolist()

    start_time = time.time()

    asyncio.run(main(urls))

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total elapsed time: {elapsed_time:.2f} seconds")
