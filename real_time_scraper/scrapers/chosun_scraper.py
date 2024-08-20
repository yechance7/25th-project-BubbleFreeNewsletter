import asyncio
import aiohttp
import json
import re
from bs4 import BeautifulSoup
import pandas as pd
import csv
import os

async def fetch_html(session, url):
    try:
        async with session.get(url) as response:
            return await response.text()
    except aiohttp.ClientError as e:
        print(f"오류가 발생했습니다: {e}")
        return None

async def get_article_content(html_source):
    soup = BeautifulSoup(html_source, 'html.parser')
    script_tag = soup.find('script', id='fusion-metadata')

    if script_tag:
        script_content = script_tag.string
        if script_content:
            json_match = re.search(r'Fusion\.globalContent\s*=\s*({.*?});', script_content)
            if json_match:
                json_content = json_match.group(1)
                try:
                    fusion_data = json.loads(json_content)
                    if 'content_elements' not in fusion_data:
                        print("JSON 응답에 'content_elements' 키가 없습니다.")
                        return None
                    content_elements = fusion_data['content_elements']
                    content_list = []
                    
                    for element in content_elements:
                        if 'content' in element:
                            content_list.append(element['content'])
                    
                    combined_content = "\n\n".join(content_list)
                    
                    # Find the starting index of the actual content
                    start_index = combined_content.find('</div>') + len('</div>')
                    cleaned_content = combined_content[start_index:]
                    
                    return cleaned_content.strip()
                except json.JSONDecodeError as e:
                    print(f"JSON을 파싱하는 중에 오류가 발생했습니다: {e}")
                    return None
            else:
                print("JSON 내용을 추출할 수 없습니다.")
                return None
        else:
            print("스크립트 태그의 내용이 비어 있습니다.")
            return None
    else:
        print("Fusion metadata 스크립트 태그를 찾을 수 없습니다.")
        return None

async def fetch_article(session, url, progress):
    html_source = await fetch_html(session, url)
    if html_source:
        article_content = await get_article_content(html_source)
        if article_content:
            progress['count'] += 1
            progress['article_list'].append([url, article_content])
            print(f"진행 상태: {progress['count']}/{progress['total']} ({(progress['count']/progress['total'])*100:.2f}%) 완료")

async def main(file_path):
    df = pd.read_csv(file_path)
    urls = df['URL'].tolist()
    
    progress = {'count': 0, 'total': len(urls), 'article_list': []}

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_article(session, url, progress) for url in urls]
        await asyncio.gather(*tasks)

    # Define the directory to save the processed CSV files
    processed_csv_dir = os.path.join('new_data', 'processed_csv')
    
    # Ensure the directory exists
    if not os.path.exists(processed_csv_dir):
        os.makedirs(processed_csv_dir)
    
    # Save to the processed_csv directory
    save_to_csv(progress['article_list'], os.path.join(processed_csv_dir, 'chosun_article.csv'))
    print("모든 URL 처리가 완료되었습니다.")

def save_to_csv(article_list, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Article"])
        for article in article_list:
            writer.writerow(article)

# 파일 경로 설정
file_path = 'new_data/raw_csv/chosun.csv'  # 올바른 CSV 파일 경로로 바꾸세요

# 비동기 함수 실행
asyncio.run(main(file_path))
