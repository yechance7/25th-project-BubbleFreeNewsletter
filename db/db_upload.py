import os
import json
import configparser
import mysql.connector
from mysql.connector import Error

# 데이터베이스 설정
config_path = "/home/yechance7/25th-project-BubbleFreeNewsletter/db"
config_file = os.path.join(config_path, "db.ini")

# ConfigParser 객체 생성 및 설정 파일 읽기
config = configparser.ConfigParser()
config.read(config_file)

try:
    # MySQL 연결
    conn = mysql.connector.connect(
        host=config.get("DB", "host"),
        port=config.getint("DB", "port"),
        user=config.get("DB", "user"),
        password=config.get("DB", "password"),
        database=config.get("DB", "database")
    )
    if conn.is_connected():
        print("데이터베이스에 성공적으로 연결되었습니다.")
        cur = conn.cursor()
except Error as err:
    print(f"오류: {err}")
    exit(1)

# 여러 JSON 파일 경로 리스트
data_path = "/home/yechance7/25th-project-BubbleFreeNewsletter/db/json"
json_files = [
    os.path.join(data_path, "hani.json"),
]

def create_database():
    """
    테이블 생성
    """
    # article 테이블 생성
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS article (
            article_id INT PRIMARY KEY,
            title TEXT,
            content TEXT,
            date DATE,
            news_company_id INT
        )
        """
    )
    conn.commit()

def insert_json_to_table(json_file_path):
    """
    JSON 데이터를 테이블에 삽입하는 함수
    """
    with open(json_file_path, "r", encoding="UTF-8") as file:
        json_list = json.load(file)

        for json_data in json_list:
            # 데이터 삽입
            cur.execute(
                """
                INSERT INTO article (article_id, title, content, date, news_company_id)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                    title=VALUES(title),
                    content=VALUES(content),
                    date=VALUES(date),
                    news_company_id=VALUES(news_company_id)
                """,
                (
                    json_data["article_id"],
                    json_data.get("title"),
                    json_data.get("content"),
                    json_data.get("date"),
                    json_data.get("news_company_id"),
                )
            )
    conn.commit()

def insert_all_json_to_db(json_files):
    """
    모든 JSON 파일을 데이터베이스에 삽입
    """
    for json_file in json_files:
        insert_json_to_table(json_file)

    conn.close()

# 함수 호출
create_database()
insert_all_json_to_db(json_files)

print("done!")
