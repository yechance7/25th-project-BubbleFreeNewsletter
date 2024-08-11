import os
import json
import configparser
import mysql.connector
from mysql.connector import Error


# 여러 JSON 파일 경로 리스트
data_path = "/home/yechance7/25th-project-BubbleFreeNewsletter/db/json"
json_files = [
    os.path.join(data_path, "hani.json"),
]


# 데이터베이스 설정
config_path = "/home/yechance7/25th-project-BubbleFreeNewsletter/db"
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
    테이블 생성
    """
    try:
        cursor.execute(
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
        print("테이블이 성공적으로 생성되었습니다.")
    except Error as err:
        print(f"테이블 생성 오류: {err}")

def insert_json_to_table(cursor, json_file_path):
    """
    JSON 데이터를 테이블에 삽입하는 함수
    """
    try:
        with open(json_file_path, "r", encoding="UTF-8") as file:
            json_list = json.load(file)
            for json_data in json_list:
                cursor.execute(
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
            print(f"{json_file_path}의 데이터가 성공적으로 삽입되었습니다.")
    except (Error, IOError) as err:
        print(f"데이터 삽입 오류: {err}")

def insert_all_json_to_db(cursor, json_files):
    """
    모든 JSON 파일을 데이터베이스에 삽입
    """
    for json_file in json_files:
        insert_json_to_table(cursor, json_file)
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

