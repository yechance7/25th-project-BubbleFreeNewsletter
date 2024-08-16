import streamlit as st
import requests
import os

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")  # 환경 변수 또는 기본값 설정

st.title("뉴스 기사 검색")

# 제목으로 검색
title_query = st.text_input("제목으로 검색")
if st.button("검색"):
    if title_query:
        response = requests.get(f"{BASE_URL}/search/title/{title_query}")
        if response.status_code == 200:
            articles = response.json()
            st.write("검색 결과:")
            for article in articles:
                st.write(f"**{article['title']}**")
                st.write(f"키워드: {article['keyword']}")
                st.write(f"일자: {article['date']}")
                st.write("---")
        else:
            st.error("기사를 찾을 수 없습니다.")

# 키워드로 검색
keyword_query = st.text_input("키워드로 검색")
if st.button("검색 (키워드)"):
    if keyword_query:
        response = requests.get(f"{BASE_URL}/search/keyword/{keyword_query}")
        if response.status_code == 200:
            articles = response.json()
            st.write("검색 결과:")
            for article in articles:
                st.write(f"**{article['title']}**")
                st.write(f"키워드: {article['keyword']}")
                st.write(f"일자: {article['date']}")
                st.write("---")
        else:
            st.error("기사를 찾을 수 없습니다.")

# article_id로 조회
article_id = st.text_input("기사 ID로 조회")
if st.button("조회"):
    if article_id:
        response = requests.get(f"{BASE_URL}/article/{article_id}")
        if response.status_code == 200:
            article = response.json()
            st.write(f"**{article['title']}**")
            st.write(f"키워드: {article['keyword']}")
            st.write(f"일자: {article['date']}")
            st.write(f"내용: {article['content']}")
        else:
            st.error("기사를 찾을 수 없습니다.")



'''
streamlit_demo.py
fast api에 get 요청을 하여 해당 조건에 맞는 기사 가져옴

local에서는 결과확인 잘됨.
github에 올리고 streamlit cloud 활용하면 배포가능하지만,  local 기준으로 백이랑 db가 설정되어 있어서 배포 불가 - 추후 바꿔야됨
+ github에 올릴시에 배포가 가능하나 ybigta organization에 올라가 있을때는 안됨 -> 본인계정에 fork하면 배포 가능

실행방법:
streamlit run be/streamlit_demo.py

향후 개선방안
- stramlit이 파이썬과 호완성 좋고 빠르게 짤 수 있지만 예쁘게 꾸밀수 있는데 한계가 있고 로그인 기능 구현이 매우 복잡(예시 코드 가진게 있어서 할 수는 있는데 이번 프로젝트에서는 굳이?) 
- react로 선회

'''