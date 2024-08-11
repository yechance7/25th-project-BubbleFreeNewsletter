import urllib.request
import urllib.error
import json
import re
from bs4 import BeautifulSoup

def get_html_source(url):
    try:
        response = urllib.request.urlopen(url)
        return response.read().decode('utf-8')
    except urllib.error.URLError as e:
        print(f"오류가 발생했습니다: {e}")
        return None

def get_article_content(html_source):
    soup = BeautifulSoup(html_source, 'html.parser')
    script_tag = soup.find('script', {'type': 'application/ld+json'})

    if script_tag:
        script_content = script_tag.string
        if script_content:
            try:
                fusion_data = json.loads(script_content)
                article_body = fusion_data.get('articleBody')
                if article_body:
                    return article_body
                else:
                    print("기사 본문을 찾을 수 없습니다.")
                    return None
            except json.JSONDecodeError as e:
                print(f"JSON을 파싱하는 중에 오류가 발생했습니다: {e}")
                return None
        else:
            print("스크립트 태그의 내용이 비어 있습니다.")
            return None
    else:
        print("Fusion metadata 스크립트 태그를 찾을 수 없습니다.")
        return None

article_list = []
urls = ['https://www.hani.co.kr/arti/opinion/editorial'] 
for url in urls:
    html_source = get_html_source(url)
    if html_source:
        article_content = get_article_content(html_source)
        if article_content:
            article_list.append(article_content)

for article in article_list:
    print(article)
