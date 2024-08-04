import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import csv

def get_html_source(url):
    try:
        response = urllib.request.urlopen(url)
        return response.read().decode('utf-8')
    except urllib.error.URLError as e:
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

article_list = []
urls = ['https://www.donga.com/news/Opinion/article/all/20240802/126294874/2'] 
for url in urls:
    html_source = get_html_source(url)
    if html_source:
        article_text = extract_article_text(html_source)
        article_list.append([url, article_text])

# CSV 파일로 저장
save_to_csv(article_list, 'donga.csv')
