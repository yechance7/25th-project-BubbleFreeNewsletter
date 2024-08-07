import aiohttp
import asyncio
import csv
from bs4 import BeautifulSoup
import pandas as pd

async def get_html_source(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            return await response.text()
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        print(f"오류가 발생했습니다: {e}")
        return None

def extract_article_text(html_source):
    soup = BeautifulSoup(html_source, 'html.parser')
    article_sections = soup.select('div.main_view section.news_view')
    
    article_text = ""
    for section in article_sections:
        # Extract the text, preserving line breaks
        text = section.get_text(separator="\n", strip=True)
        article_text += text + "\n"
    
    return article_text.strip()

def save_to_csv(article_list, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Article"])
        for article in article_list:
            writer.writerow(article)

async def fetch_articles(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(get_html_source(session, url))
        
        html_sources = await asyncio.gather(*tasks)
        
        article_list = []
        failed_urls = []
        for url, html_source in zip(urls, html_sources):
            if html_source:
                article_text = extract_article_text(html_source)
                article_list.append([url, article_text])
            else:
                failed_urls.append(url)
        
        return article_list, failed_urls

file_path = 'src/scrapers/donga.csv'  # Replace this with the correct path to your Excel file
# Read the Excel file into a DataFrame
df = pd.read_csv(file_path)
# Extract the URLs from the 'URL' column
urls = df['URL'].tolist()


# 비동기 작업 실행
article_list, failed_urls = asyncio.run(fetch_articles(urls))

# CSV 파일로 저장
save_to_csv(article_list, 'donga.csv')

# 오류가 난 URL 로깅
if failed_urls:
    with open('failed_urls.log', 'w', encoding='utf-8') as file:
        for url in failed_urls:
            file.write(url + '\n')
