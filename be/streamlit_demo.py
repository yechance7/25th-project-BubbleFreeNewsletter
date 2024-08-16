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
