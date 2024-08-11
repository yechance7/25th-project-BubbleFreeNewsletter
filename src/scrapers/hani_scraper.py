import requests
from bs4 import BeautifulSoup
import json
import argparse

def fetch_articles(start_page, end_page):
    base_url = 'https://www.hani.co.kr'
    articles_data = []

    for page in range(start_page, end_page + 1):
        editorial_url = f'{base_url}/arti/opinion/editorial?page={page}'
        print(f"크롤링 중: {editorial_url}")
        
        # HTTP GET 요청
        response = requests.get(editorial_url)
        response.raise_for_status()  # 오류가 발생하면 예외를 발생시킵니다.

        # BeautifulSoup 객체 생성
        soup = BeautifulSoup(response.text, 'html.parser')

        # 기사 목록 추출
        article_items = soup.select('.ArticleGalleryList_item__f39zX')

        for item in article_items:
            article_link = item.select_one('.BaseArticleCardVertical_link__3rmjA')['href']
            article_url = f'{base_url}{article_link}'
            
            # 각 기사 페이지 요청
            article_response = requests.get(article_url)
            article_response.raise_for_status()
            article_soup = BeautifulSoup(article_response.text, 'html.parser')

            # 기사 제목, 날짜 및 본문 추출
            title = article_soup.select_one('.ArticleDetailView_title__9kRU_').get_text(strip=True)
            date_edit = article_soup.select_one('.ArticleDetailView_dateListItem__mRc3d span').get_text(strip=True)
            article_content = ' '.join(p.get_text(strip=True) for p in article_soup.select('.article-text .text'))
            
            # 데이터 저장
            articles_data.append({
                'date': date_edit,
                'date_edit': date_edit,
                'href': article_url,
                'title': title,
                'article': article_content
            })

    # JSON 파일로 저장
    file_name='articles_data.json'
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(articles_data, json_file, ensure_ascii=False, indent=4)

    print(f"크롤링 및 {file_name} 파일 저장 완료.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch articles from specified page range.')
    parser.add_argument('start_page', type=int, help='Starting page number')
    parser.add_argument('end_page', type=int, help='Ending page number')

    args = parser.parse_args()

    fetch_articles(args.start_page, args.end_page)

# python hani_scraper.py 1 5  
# 페이지당 15개 기사