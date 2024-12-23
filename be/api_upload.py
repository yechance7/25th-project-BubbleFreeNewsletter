from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Text, JSON
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import configparser
from pydantic import BaseModel
from datetime import datetime
import numpy as np
import os
import torch
import torch.nn as nn
from transformers import BertForSequenceClassification, BertTokenizer
import json
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
    image = Column(String(255))
    inference = Column(JSON)

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
model_name_or_path = "../module/bubble_free_BERT"
tokenizer_name_or_path = "../module/bubble_free_tokenizer"

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

class Selection(BaseModel):
    article_id: str
    selected: bool
    logits: list

class SelectionsRequest(BaseModel):
    user_id: str
    selections: list[Selection]

@app.post("/save-selections")
async def save_selections(request: SelectionsRequest, db: Session = Depends(get_db)):
    try:
        user_id = request.user_id
        selections = request.selections
        
        logits_sum = None
        count = 0

        for selection in selections:
            if selection.selected:
                logits = selection.logits
                
                if logits_sum is None:
                    logits_sum = logits
                else:
                    logits_sum = [x + y for x, y in zip(logits_sum, logits)]
                
                count += 1
        
        if count == 0:
            raise HTTPException(status_code=400, detail="No valid selections provided.")

        average_logits = [x / count for x in logits_sum]
        average_logits_json = json.dumps(average_logits)

        user_info = db.query(UserInfo).filter(UserInfo.user_id == user_id).first()

        if user_info:
            user_info.average_logits = average_logits_json
        else:
            user_info = UserInfo(user_id=user_id, average_logits=average_logits_json)
            db.add(user_info)

        db.commit()

        return {"message": "Selections saved successfully!", "average_logits": average_logits}
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        # 여기에서 자세한 로그를 기록하는 것이 좋습니다.
        import logging
        logging.error(f"Error saving selections: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


# 코사인 유사도 계산 함수
def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)


@app.get("/user_info/{user_id}")
async def get_user_data(user_id: str, db: Session = Depends(get_db)):
    user = db.query(UserInfo).filter(UserInfo.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/todayNewsList/{user_id}/{date}")
async def get_today_news_list(user_id: str, date: int, db: Session = Depends(get_db)):

    #date = datetime.strptime(date, '%Y-%m-%d').date()
    #date_int = int(date.strftime('%Y%m%d'))

    news_list = db.query(Article).filter(Article.date == date).all()

    if not news_list:
        raise HTTPException(status_code=404, detail="No news found for this date")

    user = db.query(UserInfo).filter(UserInfo.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_logits_list = json.loads(user.average_logits)
    user_logits = np.array(user_logits_list).astype(float)

    news_with_similarity = []
    for news in news_list:
        news_logits = np.array(news.inference[0])
        similarity = cosine_similarity(user_logits, news_logits)
        news_with_similarity.append((news, similarity))

    news_with_similarity.sort(key=lambda x: x[1])
    top_3_news = [news for news, similarity in news_with_similarity[:3]]

    return top_3_news


# DB 초기화
init_db()
