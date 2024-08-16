import os
import json
import configparser
import mysql.connector
from mysql.connector import Error

# 여러 JSON 파일 경로 리스트
data_path = "json/"
json_files = [
    os.path.join(data_path, "chosun.json"),
    os.path.join(data_path, "donga.json"),
    os.path.join(data_path, "hani.json"),
    os.path.join(data_path, "joongang.json"),
    os.path.join(data_path, "khan.json"),
]

# 각 신문사의 prefix
news_prefixes = {
    "chosun": "c",
    "donga": "d",
    "hani": "h",
    "joongang": "j",
    "khan": "k"
}

# 데이터베이스 설정
config_path = "."
config_file = os.path.join(config_path, "db.ini")

# ConfigParser 객체 생성 및 설정 파일 읽기
config = configparser.ConfigParser()
config.read(config_file)

def create_database(cursor):
    """
    데이터베이스 생성
    """
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config.get('DB', 'database')}")
        cursor.execute(f"USE {config.get('DB', 'database')}")
        print("데이터베이스가 성공적으로 생성되었습니다.")
    except Error as err:
        print(f"데이터베이스 생성 오류: {err}")

def create_table(cursor):
    """
    테이블 생성 (keyword 열 추가)
    """
    try:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS article (
                article_id VARCHAR(255) PRIMARY KEY,
                title TEXT,
                keyword TEXT,
                content TEXT,
                date INT
            )
            """
        )
        print("테이블이 성공적으로 생성되었습니다.")
    except Error as err:
        print(f"테이블 생성 오류: {err}")

def insert_json_to_table(cursor, json_file_path, prefix):
    """
    JSON 데이터를 테이블에 삽입하는 함수
    """
    try:
        with open(json_file_path, "r", encoding="UTF-8") as file:
            json_list = json.load(file)
            for idx, json_data in enumerate(json_list, 1):
                article_id = f"{prefix}{idx}"  # 신문사 prefix와 번호를 결합하여 article_id 생성
                title = json_data.get("제목")
                keyword = json_data.get("키워드")
                content = json_data.get("Article", "")
                content = content if content else json_data.get("본문")  # content가 빈 문자열이면 "본문"으로 설정
                date = json_data.get("일자")

                cursor.execute(
                    """
                    INSERT INTO article (article_id, title, keyword, content, date)
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE 
                        title=VALUES(title),
                        keyword=VALUES(keyword),
                        content=VALUES(content),
                        date=VALUES(date)
                    """,
                    (article_id, title, keyword, content, date)
                )
            print(f"{json_file_path}의 데이터가 성공적으로 삽입되었습니다.")
    except (Error, IOError) as err:
        print(f"데이터 삽입 오류: {err}")

def insert_all_json_to_db(cursor, json_files):
    """
    모든 JSON 파일을 데이터베이스에 삽입
    """
    for json_file in json_files:
        prefix = news_prefixes.get(os.path.basename(json_file).split(".")[0], "unknown")
        insert_json_to_table(cursor, json_file, prefix)
    print("모든 데이터가 데이터베이스에 삽입되었습니다.")

try:
    # MySQL 연결
    conn = mysql.connector.connect(
        host=config.get("DB", "host"),
        port=config.getint("DB", "port"),
        user=config.get("DB", "user"),
        password=config.get("DB", "password")
    )
    if conn.is_connected():
        print("데이터베이스에 성공적으로 연결되었습니다.")
        cursor = conn.cursor()

        create_database(cursor)  # 데이터베이스 생성
        create_table(cursor)     # 테이블 생성
        conn.database = config.get("DB", "database")  # 데이터베이스 설정

        insert_all_json_to_db(cursor, json_files)

        conn.commit()
except Error as err:
    print(f"오류: {err}")
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("연결이 종료되었습니다.")

print("done!")



'''
db/db_upload.py: mysql 활성화하여 데이터베이스 생성 후 json파일 바탕으로 article table 생성

데이터셋 구성
article_id: PRIMARY KEY ["chosun": "c", "donga": "d","hani": "h","joongang": "j","khan": "k"] ex) c1- 조선일보 첫번째 기사
title: 기사제목
keyword: 키워드
content: 본문(만약 크롤링된 본문이 없을시 빅카인즈의 짤린 본문)
date: 기사날짜

- mysql 서버활성화에 로그인 권한 관련되서 되게 복잡함... chatgpt에게 물어보면서 해결하면 결국 됨

실행방법:
1. mysql 시작
sudo service mysql start

2. db 생성
python db_upload.py


향후 개선방안:
- 이후에 모델 훈련결과로 나온 진보-보수 라벨정도 열 추가하는 코드

'''