import asyncio
import aiohttp
from bs4 import BeautifulSoup
import csv
import pandas as pd
import os

async def fetch_html(session, url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=180)) as response:
            return await response.text()
    except asyncio.TimeoutError as e:
        print(f"타임아웃 오류가 발생했습니다: {e}")
        return 'timeout'
    except (aiohttp.ClientError, Exception) as e:
        print(f"오류가 발생했습니다: {e}")
        return None

async def extract_article_text(html_source):
    soup = BeautifulSoup(html_source, 'html.parser')
    
    # Extract article text
    article_sections = soup.find_all('p', class_='text')
    article_text = ""
    for section in article_sections:
        text = section.get_text(separator="\n", strip=True)
        article_text += text + "\n"

    # Extract specific image source using the provided CSS selector
    image_tag = soup.select_one('#renewal2023 > div.article-text > div.ArticleDetailContent_imageContainer___o_gm > figure > div > img')
    image_src = image_tag['src'] if image_tag else None

    return article_text.strip(), image_src

async def fetch_article(session, url, progress, timeout_urls):
    html_source = await fetch_html(session, url)
    if html_source == 'timeout':
        timeout_urls.append(url)
        progress['count'] += 1
        print(f"진행 상태: {progress['count']}/{progress['total']} ({(progress['count']/progress['total'])*100:.2f}%) 완료 (타임아웃 발생)")
    elif html_source:
        article_text, image_src = await extract_article_text(html_source)
        if article_text or image_src:
            progress['count'] += 1
            progress['article_list'].append([url, article_text, image_src])
            print(f"진행 상태: {progress['count']}/{progress['total']} ({(progress['count']/progress['total'])*100:.2f}%) 완료")
        else:
            progress['count'] += 1
            print(f"진행 상태: {progress['count']}/{progress['total']} ({(progress['count']/progress['total'])*100:.2f}%) 완료 (컨텐츠 없음)")
    else:
        progress['count'] += 1
        print(f"진행 상태: {progress['count']}/{progress['total']} ({(progress['count']/progress['total'])*100:.2f}%) 완료 (오류 발생)")

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

    # Specify the output filename
    filename = 'new_data/processed_csv/hani_article.csv'
    
    # Delete the file if it exists
    if os.path.exists(filename):
        os.remove(filename)
    
    # Save the articles and image sources to CSV
    save_to_csv(progress['article_list'], filename)

    print("모든 URL 처리가 완료되었습니다.")

def save_to_csv(article_list, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Article", "Image"])
        for article in article_list:
            writer.writerow(article)

# URL 리스트
file_path = 'new_data/raw_csv/hani.csv'  # Replace this with the correct path to your CSV file
# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)
# Extract the URLs from the 'URL' column
urls = df['URL'].tolist()

# 비동기 함수 실행
asyncio.run(main(urls))
