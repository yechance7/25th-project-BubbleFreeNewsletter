import React, { useState, useEffect } from 'react';
import { fetchUserData, fetchNewsListByDate } from '../api';
import KeywordButtons from '../components/KeywordButtons';
import ArticleContent from '../components/ArticleContent';
import './NewsletterPage.css'; // CSS 파일을 임포트

const NewsletterPage = () => {
    const [userId, setUserId] = useState('');
    const [userData, setUserData] = useState(null);
    const [newsList, setNewsList] = useState([]);
    const [selectedNews, setSelectedNews] = useState('');
    const [currentDate, setCurrentDate] = useState(new Date()); // date of today
    const [loading, setLoading] = useState(false); // 로딩 상태 추가

    const formatDateToInt = (date) => {
        return `${date.getFullYear()}${String(date.getMonth() + 1).padStart(2, '0')}${String(date.getDate()).padStart(2, '0')}`;
    };

    useEffect(() => {
        const fetchNews = async () => {
            if (userData) {
                setLoading(true); // 뉴스 목록 로드 시작
                try {
                    const formattedDate = formatDateToInt(currentDate);
                    const news = await fetchNewsListByDate(userId, formattedDate);
                    setNewsList(news);
                } catch (error) {
                    console.error('Error fetching news list:', error);
                } finally {
                    setLoading(false); // 뉴스 목록 로드 완료
                }
            }
        };
    
        fetchNews();
    }, [userData, currentDate]);

    const handleUserIdSubmit = async () => {
        try {
            const data = await fetchUserData(userId);
            setUserData(data);
    
            const formattedDate = formatDateToInt(currentDate);
            const news = await fetchNewsListByDate(userId, formattedDate);
            setNewsList(news);
        } catch (error) {
            console.error('Error fetching user data or news list:', error);
        }
    };

    const handlePrevDate = () => {
        setCurrentDate(prevDate => {
            const newDate = new Date(prevDate);
            newDate.setDate(newDate.getDate() - 1);
            return newDate;
        });
    };

    const handleNextDate = () => {
        setCurrentDate(prevDate => {
            const newDate = new Date(prevDate);
            newDate.setDate(newDate.getDate() + 1);
            return newDate;
        });
    };

    return (
        <div className="newsletter-container">
            {!userData ? (
                <div className="input-section">
                    <h1>닉네임을 입력하세요!</h1>
                    <input 
                        type="text" 
                        value={userId} 
                        onChange={(e) => setUserId(e.target.value)} 
                        placeholder="Enter user ID" 
                    />
                    <button onClick={handleUserIdSubmit}>Submit</button>
                </div>
            ) : (
                <div className="content-wrapper">
                    <h1>BubblePOP NewsLetter 📰</h1>
                    {loading ? (
                        <p>뉴스를 불러오는 중...</p>
                    ) : (
                        <>
                            <KeywordButtons newsList={newsList} onSelect={setSelectedNews} />
                            {selectedNews && <ArticleContent news={selectedNews} />}
                        </>
                    )}
                </div>
            )}
            <div className="footer">
                <button onClick={handlePrevDate}>이전</button>
                <span>{formatDateToInt(currentDate)}</span>
                <button onClick={handleNextDate}>다음</button>
            </div>
        </div>
    );
};

export default NewsletterPage;
