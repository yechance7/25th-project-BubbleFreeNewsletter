import os
import json
import mysql.connector
from mysql.connector import Error
import configparser
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import torch.nn as nn

'''
add_inference.py
모델을 불러와서 inference한 결과를 db에 새로운 열로서 추가
db_upload.py 실행후에 추가

데이터 행을 한줄한줄 불러오고 모델도 돌려야하기에 시간이 상당히 걸림

실행방법:
python add_inference.py

'''


def load_model():
    """
    모델과 토크나이저 로드
    """
    model_name_or_path = "../module/bubble_free_BERT"
    tokenizer_name_or_path = "../module/bubble_free_tokenizer"

    model = AutoModelForSequenceClassification.from_pretrained(model_name_or_path)
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name_or_path)
    
    return model, tokenizer

def predict(model, tokenizer, content):
    """
    모델을 사용하여 추론 수행
    """
    model.eval()

    device = torch.device("cuda" if torch.cuda.is_available() else "mps")
    model.to(device)

    inputs = tokenizer(content, return_tensors="pt", max_length=128, truncation=True, padding="max_length")

    inputs = {key: value.to(device) for key, value in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits

        softmax = nn.Softmax(dim=1)  # dim=1은 클래스 차원에 대해 softmax를 적용
        preds = softmax(logits)

    logits = logits.cpu().numpy().round(4)
    preds = logits.cpu().numpy().round(4)

    return json.dumps(preds.tolist())

def add_inference_column(cursor):
    """
    데이터베이스에 새로운 열 'inference'를 추가합니다.
    이미 존재하는 경우 추가하지 않습니다.
    """
    try:
        # Check if the column already exists
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM information_schema.columns
            WHERE table_name = 'article' AND column_name = 'inference'
            """
        )
        exists = cursor.fetchone()[0]

        if exists:
            print("열 'inference'가 이미 존재합니다.")
        else:
            # Add the column if it does not exist
            cursor.execute(
                """
                ALTER TABLE article
                ADD COLUMN inference JSON
                """
            )
            print("새로운 열 'inference'가 추가되었습니다.")
    except Error as err:
        print(f"열 추가 오류: {err}")


def update_inference(cursor, article_id, inference):
    """
    데이터베이스에 예측 결과를 업데이트합니다.
    이미 예측 결과가 있는 경우 업데이트하지 않습니다.
    """
    try:
        # Check if the inference column is NULL for the given article_id
        cursor.execute(
            """
            SELECT inference
            FROM article
            WHERE article_id = %s
            """,
            (article_id,)
        )
        current_inference = cursor.fetchone()

        if current_inference is not None and current_inference[0] is not None:
            pass
        else:
            # Update the inference if it is currently NULL
            cursor.execute(
                """
                UPDATE article
                SET inference = %s
                WHERE article_id = %s
                """,
                (inference, article_id)
            )
            print(f"article_id {article_id}의 예측 결과가 업데이트되었습니다.")
    except Error as err:
        print(f"예측 결과 업데이트 오류: {err}")

# 데이터베이스 설정
config_path = "."
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
        cursor = conn.cursor()

        # 새로운 열 'new_inference' 추가
        add_inference_column(cursor)
        
        # 모델 로드
        model, tokenizer = load_model()
        
        # 데이터베이스에서 inference 값이 없는 데이터만 불러오기
        cursor.execute("SELECT article_id, content FROM article WHERE inference IS NULL")
        rows = cursor.fetchall()

        for row in rows:
            article_id, content = row
            inference = predict(model, tokenizer, content)
            update_inference(cursor, article_id, inference)

        conn.commit()

except Error as err:
    print(f"오류: {err}")
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("연결이 종료되었습니다.")
