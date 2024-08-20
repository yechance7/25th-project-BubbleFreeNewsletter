import os
import asyncio
import aiohttp
import json
import re
from bs4 import BeautifulSoup
import pandas as pd
import csv

async def fetch_html(session, url):
    try:
        async with session.get(url) as response:
            return await response.text()
    except aiohttp.ClientError as e:
        print(f"Error occurred: {e}")
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
                        print("The 'content_elements' key is missing in the JSON response.")
                        return None
                    content_elements = fusion_data['content_elements']
                    content_list = []
                    image_list = []

                    for element in content_elements:
                        if 'content' in element:
                            content_list.append(element['content'])
                        if 'type' in element and element['type'] == 'image':
                            if 'url' in element:
                                image_list.append(element['url'])

                    combined_content = "\n\n".join(content_list)

                    # Clean up the content if needed
                    start_index = combined_content.find('</div>') + len('</div>')
                    cleaned_content = combined_content[start_index:].strip()

                    return cleaned_content, image_list
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON: {e}")
                    return None, None
            else:
                print("Could not extract JSON content.")
                return None, None
        else:
            print("Script tag content is empty.")
            return None, None
    else:
        print("Could not find the Fusion metadata script tag.")
        return None, None

async def fetch_article(session, url, progress):
    html_source = await fetch_html(session, url)
    if html_source:
        article_content, image_links = await get_article_content(html_source)
        if article_content:
            progress['count'] += 1
            progress['article_list'].append([url, article_content, ";".join(image_links)])
            print(f"Progress: {progress['count']}/{progress['total']} ({(progress['count']/progress['total'])*100:.2f}%) completed")

async def main(file_path):
    df = pd.read_csv(file_path)
    urls = df['URL'].tolist()
    
    progress = {'count': 0, 'total': len(urls), 'article_list': []}

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_article(session, url, progress) for url in urls]
        await asyncio.gather(*tasks)

    processed_csv_dir = os.path.join('new_data', 'processed_csv')
    
    if not os.path.exists(processed_csv_dir):
        os.makedirs(processed_csv_dir)
    
    csv_file_path = os.path.join(processed_csv_dir, 'chosun_article.csv')
    
    save_to_csv(progress['article_list'], csv_file_path)
    print("All URLs have been processed.")

def save_to_csv(article_list, filename):
    # Remove the file if it already exists
    if os.path.exists(filename):
        os.remove(filename)
        print(f"Existing file '{filename}' has been removed.")

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Article", "Image"])
        for article in article_list:
            writer.writerow(article)

file_path = 'new_data/raw_csv/chosun.csv'  # Replace with the correct CSV file path

asyncio.run(main(file_path))
