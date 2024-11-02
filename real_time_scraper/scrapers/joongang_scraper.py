import asyncio
import aiohttp
from bs4 import BeautifulSoup
import csv
import os
import pandas as pd

async def fetch_html(session, url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=180)) as response:
            return await response.text()
    except asyncio.TimeoutError as e:
        print(f"Timeout error: {e}")
        return 'timeout'
    except (aiohttp.ClientError, Exception) as e:
        print(f"Error occurred: {e}")
        return None

async def extract_article_text_and_image(html_source):
    soup = BeautifulSoup(html_source, 'html.parser')
    
    # Extract article text
    article_sections = soup.select('div.article_body p')
    article_text = ""
    for section in article_sections:
        text = section.get_text(separator="\n", strip=True)
        article_text += text + "\n"
    
    article_text = article_text.strip()

    # Extract image src using the provided selector
    image_tag = soup.select_one('#article_body > div.ab_photo.photo_center > div > img')
    if image_tag:
        image_src = image_tag['src']
        # Remove "/_ir50_/" from the image link if it exists
        if "/_ir50_/" in image_src:
            image_src = image_src.replace("/_ir50_/", "")
    else:
        image_src = None

    return article_text, image_src

async def fetch_article(session, url, progress, timeout_urls):
    html_source = await fetch_html(session, url)
    if html_source == 'timeout':
        timeout_urls.append(url)
        progress['count'] += 1
        print(f"Progress: {progress['count']}/{progress['total']} ({(progress['count']/progress['total'])*100:.2f}%) complete (timeout)")
    elif html_source:
        article_text, image_src = await extract_article_text_and_image(html_source)
        if article_text or image_src:
            progress['count'] += 1
            progress['article_list'].append([url, article_text, image_src])
            print(f"Progress: {progress['count']}/{progress['total']} ({(progress['count']/progress['total'])*100:.2f}%) complete")
        else:
            progress['count'] += 1
            print(f"Progress: {progress['count']}/{progress['total']} ({(progress['count']/progress['total'])*100:.2f}%) complete (no content)")
    else:
        progress['count'] += 1
        print(f"Progress: {progress['count']}/{progress['total']} ({(progress['count']/progress['total'])*100:.2f}%) complete (error)")

async def main(urls):
    progress = {'count': 0, 'total': len(urls), 'article_list': []}
    timeout_urls = []
    remaining_urls = urls.copy()

    async with aiohttp.ClientSession() as session:
        while remaining_urls:
            current_batch = remaining_urls[:10]
            remaining_urls = remaining_urls[10:]

            tasks = [fetch_article(session, url, progress, timeout_urls) for url in current_batch]
            await asyncio.gather(*tasks)

            if timeout_urls:
                break

    save_to_csv(progress['article_list'], 'new_data/processed_csv/joongang_article.csv')
    print("All URLs have been processed.")

def save_to_csv(article_list, filename):
    # Remove the existing file if it exists
    if os.path.exists(filename):
        os.remove(filename)
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Article", "Image"])
        for article in article_list:
            writer.writerow(article)

def save_failed_urls(failed_urls, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for url in failed_urls:
            file.write(url + '\n')

# URL list
file_path = 'new_data/raw_csv/joongang.csv'  # Replace this with the correct path to your CSV file
df = pd.read_csv(file_path)
urls = df['URL'].tolist()

# Run the async function
asyncio.run(main(urls))
