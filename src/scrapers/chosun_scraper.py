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
    # 'fusion-metadata' ID를 가진 <script> 태그를 찾음
    script_tag = soup.find('script', id='fusion-metadata')
    
    if script_tag:
        script_content = script_tag.string
        if script_content:
            json_match = re.search(r'Fusion\.globalContent\s*=\s*({.*?});', script_content)
            if json_match:
                json_content = json_match.group(1)
                try:
                    # 추출한 JSON 내용을 파싱
                    fusion_data = json.loads(json_content)
                    content_elements = fusion_data['content_elements']
                    content_list = []
                    
                    for element in content_elements:
                        if 'content' in element:
                            content_list.append(element['content'])
                    
                    return "\n\n".join(content_list)
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

article_list = []
urls = ['https://www.chosun.com/opinion/editorial/2024/08/02/YAKPOY2HNFCYRJDBAVA4KT3FLQ/', 'https://www.chosun.com/opinion/editorial/2024/08/01/74ICUQOVRNE27J5LZV3AZOINMI/','https://www.chosun.com/opinion/editorial/2024/08/02/GK5NZZLCCBEEPH4GMUDKPAVSW4/' ] 
for url in urls:
    html_source = get_html_source(url)
    if html_source:
        article_content = get_article_content(html_source)
        if article_content:
            article_list.append(article_content)


            



