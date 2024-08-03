import urllib.request
import urllib.error
import json
import re
from bs4 import BeautifulSoup

def get_html_source(url) -> str:
    try:
        # HTTP Error 403: Forbidden 우회
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        )
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except urllib.error.URLError as e:
        print(f"오류가 발생했습니다: {e}")
        return ''
    
def get_article_content(html_source) -> str:
    soup = BeautifulSoup(html_source, 'html.parser')
    # 본문 내용이 담긴 파트를 찾는다.
    try:
        article_body = soup.find('div', {'id': 'articleBody'})
    except Exception as e:
        print(f"Error: {e}")
    
    text_content = article_body.get_text(separator='\n').strip()
    text_content = re.sub(r'\n\s*\n', '\n', text_content)

    return text_content
    

if __name__ == "__main__":
    # output_json = 'output.json'
    article_data = []
    article_list : list[str] = []

    urls : list[str] = ['https://www.khan.co.kr/sports/olympic-asian_games/article/202408031844001', 'https://www.khan.co.kr/politics/politics-general/article/202408031432001'] 
    for url in urls:
        try:
            html_source : str = get_html_source(url)
            if html_source:
                article_content : str = get_article_content(html_source)
                if article_content:
                    article_list.append(article_content)

                    # # for json store
                    # article_json = {
                    #     "article": article_content
                    # }
                    # article_data.append(article_json)

        except Exception as e:
            print(f"Error: {e}")
        # finally:
        #     with open(output_json, 'w', encoding='utf-8') as f:
        #         json.dump(article_data, f, ensure_ascii=False, indent=4)