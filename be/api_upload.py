from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import configparser
import os
import torch
import torch.nn as nn
from transformers import BertForSequenceClassification, BertTokenizer
import json
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

# FastAPI 애플리케이션 설정
app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 프론트엔드 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 나머지 코드...


'''
api_upload.py: 활성화시 SQLAlchemy 바탕으로 데이터베이스와 연결 get 요청에 응답하여 해당하는 기사 가져다줌

실행방법:
python api_upload.py
uvicorn api_upload:app --reload
두 개 다 실행되어야함. 터미널 유지해야 돌아감

향후 개선방안
- 추후에 모델 불러오는것 추가
- 모델을 바탕으로 어떠한 방식으로 기사데이터를 보여줄건지 자세한 로직

'''

# 데이터베이스 설정
config_path = "../db"  # 데이터베이스 설정 파일이 위치한 디렉토리의 상대 경로
config = configparser.ConfigParser()
config.read(os.path.join(config_path, "db.ini"))

# 데이터베이스 URL 설정
DATABASE_URL = f"mysql+mysqlconnector://{config['DB']['user']}:{config['DB']['password']}@{config['DB']['host']}:{config['DB']['port']}/{config['DB']['database']}"

# SQLAlchemy 설정
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 모델 정의
class Article(Base):
    __tablename__ = "article"
    
    article_id = Column(String(255), primary_key=True, index=True)  # VARCHAR(255) in MySQL
    title = Column(Text, index=True)
    keyword = Column(Text)
    content = Column(Text)
    date = Column(Integer)  # MySQL의 INT 타입과 호환되도록 Integer 사용
    softmax_probabilities = Column(Text)  # BERT 모델 추론 후 softmax 확률 저장
    logits = Column(Text)  # BERT 모델 추론 후 logits 저장

# # FastAPI 애플리케이션 설정
# app = FastAPI()

# 비동기 데이터베이스 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# BERT 모델 및 토크나이저 로드
model_name_or_path = "../bubble_free_BERT"
tokenizer_name_or_path = "../bubble_free_tokenizer"

model = BertForSequenceClassification.from_pretrained(model_name_or_path)
tokenizer = BertTokenizer.from_pretrained(tokenizer_name_or_path)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

@app.get("/")
async def root():
    return {"message": "Welcome to my FastAPI application!"}

# 제목으로 기사를 검색하는 엔드포인트
@app.get("/search/title/{query}")
async def search_by_title(query: str, db: Session = Depends(get_db)):
    results = db.query(Article).filter(Article.title.ilike(f"%{query}%")).all()
    
    if not results:
        raise HTTPException(status_code=404, detail="No articles found")
    
    return results

# 키워드로 기사를 검색하는 엔드포인트
@app.get("/search/keyword/{query}")
async def search_by_keyword(query: str, db: Session = Depends(get_db)):
    results = db.query(Article).filter(Article.keyword.ilike(f"%{query}%")).all()
    
    if not results:
        raise HTTPException(status_code=404, detail="No articles found")
    
    return results

# article_id로 기사를 조회하는 엔드포인트
@app.get("/article/{article_id}")
async def get_article(article_id: str, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.article_id == article_id).first()
    
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    return article

@app.post("/article/infer/{article_id}")
async def infer_article(article_id: str):
    db = SessionLocal()
    try:
        # 데이터베이스에서 article_id로 기사를 검색
        article = db.query(Article).filter(Article.article_id == article_id).first()

        if not article:
            raise HTTPException(status_code=404, detail="Article not found")

        # 기사의 내용 추출
        content = article.content

        # 입력받은 기사 본문을 모델에 전달하여 추론 수행
        inputs = tokenizer(content, return_tensors="pt", max_length=512, truncation=True, padding="max_length")
        inputs = {key: value.to(device) for key, value in inputs.items()}

        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits

            softmax = nn.Softmax(dim=1)
            preds = softmax(logits)

        # 확률과 logits를 numpy 배열로 변환
        preds_rounded = preds.cpu().numpy().tolist()
        logits_rounded = logits.cpu().numpy().tolist()

        # JSON 문자열로 변환
        preds_json = json.dumps(preds_rounded)
        logits_json = json.dumps(logits_rounded)

        # 데이터베이스에서 해당 기사 레코드를 업데이트
        article.softmax_probabilities = preds_json
        article.logits = logits_json
        db.commit()

        return {"softmax_probabilities": preds_rounded, "logits": logits_rounded}

    finally:
        db.close()

@app.get("/articles/latest")
async def get_latest_articles(db: Session = Depends(get_db)):
    articles = db.query(Article).order_by(Article.date.desc()).limit(20).all()
    return articles


@app.get("/article/logits/{article_id}")
async def get_article_logits(article_id: str, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.article_id == article_id).first()
    
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # logits를 JSON 문자열에서 리스트로 변환
    logits = json.loads(article.logits)
    
    return {"logits": logits}

@app.post("/save-average-logits")
async def save_average_logits(data: dict, db: Session = Depends(get_db)):
    average_logits = data.get('averageLogits')
    
    if not average_logits:
        raise HTTPException(status_code=400, detail="Average logits not provided")

    # 평균 logits 값을 DB에 저장하는 로직을 추가
    # 예를 들어, 로그 파일에 기록하거나 별도의 테이블에 저장할 수 있습니다.

    return {"message": "Average logits saved successfully!"}

