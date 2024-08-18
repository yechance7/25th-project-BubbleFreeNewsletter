// src/pages/MyPage.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './MyPage.css';

const MyPage = () => {
    const [currentIndex, setCurrentIndex] = useState(0);
    const [articles, setArticles] = useState([]);
    const [selectedArticles, setSelectedArticles] = useState(new Set());
    const [logitsSum, setLogitsSum] = useState(null); // logits의 합을 저장
    const [logitsCount, setLogitsCount] = useState(0); // 선택된 기사 수
    const [error, setError] = useState(null);

    useEffect(() => {
        // 초기 데이터 로딩
        axios.get('http://127.0.0.1:8000/articles/latest')
            .then(response => {
                setArticles(response.data);
            })
            .catch(err => {
                setError('Failed to load articles.');
            });
    }, []);

    const handleSelect = async (articleId) => {
        try {
            // 선택된 기사 추가
            setSelectedArticles(prev => new Set(prev).add(articleId));

            // 데이터베이스에서 해당 기사의 logits 값을 가져옴
            const { data } = await axios.get(`http://127.0.0.1:8000/article/logits/${articleId}`);
            const logits = data.logits;

            // logits 값을 누적
            setLogitsSum(prevSum => {
                if (prevSum === null) {
                    return logits;
                }
                return prevSum.map((val, index) => val + logits[index]);
            });

            setLogitsCount(prevCount => prevCount + 1);

            // 현재 인덱스가 마지막 기사가 아닌 경우 다음 인덱스로 이동
            if (currentIndex + 2 < articles.length) {
                setCurrentIndex(prev => prev + 2);
            } else {
                submitSelections();
            }
        } catch (err) {
            setError('Failed to fetch logits.');
        }
    };

    const submitSelections = async () => {
        try {
            const allLogits = [];
            for (const articleId of Object.keys(selectedOptions)) {
                const response = await axios.get(`http://127.0.0.1:8000/article/logits/${articleId}`);
                const { logits } = response.data;
                allLogits.push(logits);
            }
    
            // 평균 logits 계산
            const averageLogits = allLogits[0].map((_, index) => 
                allLogits.reduce((sum, logits) => sum + logits[index], 0) / allLogits.length
            );
    
            // 평균 logits를 저장하는 서버에 요청
            await axios.post('http://127.0.0.1:8000/save-average-logits', {
                averageLogits
            });
    
            alert('Selections and average logits saved successfully!');
        } catch (err) {
            setError('Failed to save selections and average logits.');
        }
    };
    
    const currentArticles = articles.slice(currentIndex, currentIndex + 2);

    return (
        <div className="MyPage">
            {currentArticles.length > 0 ? (
                <div className="articles-container">
                    {currentArticles.map(article => (
                        <div key={article.article_id} className="article-container">
                            <h2>{article.title}</h2>
                            <p>{article.content}</p>
                            <div className="button-group">
                                <button onClick={() => handleSelect(article.article_id)}>Select</button>
                            </div>
                        </div>
                    ))}
                </div>
            ) : (
                <p>No more articles to review.</p>
            )}
            {error && <p className="error">{error}</p>}
        </div>
    );
};

export default MyPage;
