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
    allow_origins=["*"],  # 프론트엔드 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# Article 모델 정의
class Article(Base):
    __tablename__ = "article"
    
    article_id = Column(String(255), primary_key=True, index=True)  # VARCHAR(255) in MySQL
    title = Column(Text, index=True)
    keyword = Column(Text)
    content = Column(Text)
    date = Column(Integer)  # MySQL의 INT 타입과 호환되도록 Integer 사용
    # softmax_probabilities = Column(Text)  # BERT 모델 추론 후 softmax 확률 저장
    # logits = Column(Text)  # BERT 모델 추론 후 logits 저장

# UserInfo 모델 정의
class UserInfo(Base):
    __tablename__ = "user_info"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), index=True)
    average_logits = Column(Text)  # JSON 문자열로 저장

# 테이블 생성 함수
def init_db():
    Base.metadata.create_all(bind=engine)

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

print("done!")

