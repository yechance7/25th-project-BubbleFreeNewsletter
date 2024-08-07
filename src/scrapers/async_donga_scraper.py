import asyncio
import aiohttp
from bs4 import BeautifulSoup
import csv
import pandas as pd

async def fetch_html(session, url, retry_count=3):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    for attempt in range(retry_count):
        try:
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=180)) as response:
                return await response.text()
        except aiohttp.ClientError as e:
            print(f"클라이언트 오류가 발생했습니다: {e}. 재시도 중... ({attempt + 1}/{retry_count})")
        except asyncio.TimeoutError as e:
            print(f"타임아웃 오류가 발생했습니다: {e}. 재시도 중... ({attempt + 1}/{retry_count})")
        except Exception as e:
            print(f"예기치 않은 오류가 발생했습니다: {e}. 재시도 중... ({attempt + 1}/{retry_count})")
        await asyncio.sleep(2)  # 잠시 대기 후 재시도
    return None

async def extract_article_text(html_source):
    soup = BeautifulSoup(html_source, 'html.parser')
    article_sections = soup.select('div.main_view section.news_view')
    
    article_text = ""
    for section in article_sections:
        # Extract the text, preserving line breaks
        text = section.get_text(separator="\n", strip=True)
        article_text += text + "\n"
    
    return article_text.strip()

async def fetch_article(session, url, progress):
    html_source = await fetch_html(session, url)
    if html_source:
        article_text = await extract_article_text(html_source)
        if article_text:
            progress['count'] += 1
            progress['article_list'].append([url, article_text])
            print(f"진행 상태: {progress['count']}/{progress['total']} ({(progress['count']/progress['total'])*100:.2f}%) 완료")
        else:
            progress['count'] += 1
            print(f"진행 상태: {progress['count']}/{progress['total']} ({(progress['count']/progress['total'])*100:.2f}%) 완료 (컨텐츠 없음)")

async def main(urls):
    progress = {'count': 0, 'total': len(urls), 'article_list': []}

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_article(session, url, progress) for url in urls]
        await asyncio.gather(*tasks)

    save_to_csv(progress['article_list'], 'donga_article.csv')
    print("모든 URL 처리가 완료되었습니다.")

def save_to_csv(article_list, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Article"])
        for article in article_list:
            writer.writerow(article)

# URL 리스트
urls = ['https://www.donga.com/news/Opinion/article/all/20240802/126294874/2'] 

# 비동기 함수 실행
asyncio.run(main(urls))



# URL 리스트
file_path = 'src/scrapers/donga.csv'  # Replace this with the correct path to your Excel file
# Read the Excel file into a DataFrame
df = pd.read_csv(file_path)
# Extract the URLs from the 'URL' column
urls = df['URL'].tolist()
urls = urls[7000:]

# 비동기 함수 실행
asyncio.run(main(urls))
