import asyncio
import aiohttp
import chardet
from bs4 import BeautifulSoup
import csv
import re
import pandas as pd

async def fetch_html(session, url):
    if not isinstance(url, str):
        return None
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=180)) as response:
         # Get the raw content
            raw_content = await response.read()

            # Try to detect encoding if not specified
            detected_encoding = chardet.detect(raw_content)['encoding']
            encoding = response.charset or detected_encoding or 'utf-8'

            # Decode the content with the detected or specified encoding
            try:
                return raw_content.decode(encoding)
            except UnicodeDecodeError:
                return raw_content.decode('utf-8', errors='ignore')
        
    except asyncio.TimeoutError as e:
        print(f"타임아웃 오류가 발생했습니다: {e}")
        return 'timeout'
    except (aiohttp.ClientError, Exception) as e:
        print(f"오류가 발생했습니다: {e}")
        return None

async def extract_article_text(html_source):
    soup = BeautifulSoup(html_source, 'html.parser')
    # 본문 내용이 담긴 파트를 찾는다.
    try:
        #article_body = soup.find('div', {'id': 'articleBody'})
        article_body = soup.find('div', {'class': 'art_body'})
    except Exception as e:
        print(f"Error: {e}")

    if article_body is None:
        print("Warning: 'articleBody' not found. English News")
        return None
    
    text_content = article_body.get_text(separator='\n').strip()
    text_content = re.sub(r'\n\s*\n', '\n', text_content)

    return text_content

async def fetch_article(session, url, progress, timeout_urls):
    html_source = await fetch_html(session, url)
    if html_source == 'timeout':
        timeout_urls.append(url)
        progress['count'] += 1
        print(f"진행 상태: {progress['count']}/{progress['total']} ({(progress['count']/progress['total'])*100:.2f}%) 완료 (타임아웃 발생)")
    elif html_source == None:
        progress['count'] += 1
        print(f"진행 상태: {progress['count']}/{progress['total']} ({(progress['count']/progress['total'])*100:.2f}%) 완료 (링크 없음)")
    elif html_source:
        article_text = await extract_article_text(html_source)
        if article_text:
            progress['count'] += 1
            progress['article_list'].append([url, article_text])
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

    save_to_csv(progress['article_list'], 'khan_article.csv')
    save_failed_urls(timeout_urls, 'timeout_urls.txt')
    print("모든 URL 처리가 완료되었습니다.")

def save_to_csv(article_list, filename):
    with open(filename, mode='w', newline='', encoding='utf-8', errors='ignore') as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Article"])
        for article in article_list:
            writer.writerow(article)

def save_failed_urls(failed_urls, filename):
    with open(filename, 'w', encoding='utf-8', errors='ignore') as file:
        for url in failed_urls:
            file.write(url + '\n')

# URL 리스트
file_path = '../raw_data/khan.csv'  # Replace this with the correct path to your CSV file
# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)
# Extract the URLs from the 'URL' column
urls = df['URL'].tolist()

# 비동기 함수 실행
asyncio.run(main(urls))