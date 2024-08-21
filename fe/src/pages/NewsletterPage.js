import React, { useState, useEffect } from 'react';
import { fetchUserData, fetchNewsListByDate } from '../api';
import KeywordButtons from '../components/KeywordButtons';
import ArticleContent from '../components/ArticleContent';
import './NewsletterPage.css'; 

const NewsletterPage = () => {
    const [userId, setUserId] = useState('');
    const [userData, setUserData] = useState(null);
    const [newsList, setNewsList] = useState([]);
    const [selectedNews, setSelectedNews] = useState(''); 
    const [currentDate, setCurrentDate] = useState(new Date());
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const formatDateToInt = (date) => {
        return `${date.getFullYear()}${String(date.getMonth() + 1).padStart(2, '0')}${String(date.getDate()).padStart(2, '0')}`;
    };

    const formatDateToDisplay = (date) => {
        return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
    };

    useEffect(() => {
        const fetchNews = async () => {
            if (userData) {
                setLoading(true); 
                try {
                    const formattedDate = formatDateToInt(currentDate);
                    const news = await fetchNewsListByDate(userId, formattedDate);
                    setNewsList(news || []); 
                    setSelectedNews(''); 
                } catch (error) {
                    console.error('Error fetching news list:', error);
                    setNewsList([]); 
                } finally {
                    setLoading(false); 
                }
            }
        };

        fetchNews();
    }, [userData, currentDate]);

    const handleUserIdSubmit = async () => {
        try {
            setError(''); 
            const data = await fetchUserData(userId);
            if (data) {
                setUserData(data);
                const formattedDate = formatDateToInt(currentDate);
                const news = await fetchNewsListByDate(userId, formattedDate);
                setNewsList(news || []);
            } else {
                throw new Error('User not found');
            }
        } catch (error) {
            console.error('Error fetching user data:', error);
            setError('존재하지 않는 닉네임입니다. 다시 입력해 주세요.'); 
            setUserData(null); 
            setNewsList([]); 
        }
    };

    const handlePrevDate = () => {
        setCurrentDate(prevDate => {
            const newDate = new Date(prevDate);
            newDate.setDate(newDate.getDate() - 1);
            setNewsList([]); 
            return newDate;
        });
        setSelectedNews('');
    };

    const handleNextDate = () => {
        setCurrentDate(prevDate => {
            const newDate = new Date(prevDate);
            newDate.setDate(newDate.getDate() + 1);
            setNewsList([]); 
            return newDate;
        });
        setSelectedNews('');
    };

    const isToday = (date) => {
        const today = new Date();
        return (
            date.getFullYear() === today.getFullYear() &&
            date.getMonth() === today.getMonth() &&
            date.getDate() === today.getDate()
        );
    };

    return (
        <div className="newsletter-container">
        {!userData ? (
            <div className="input-section">
                <h1>닉네임을 입력하세요!</h1>
                {error && <p className="error-message">{error}</p>} {/* 에러 메시지 표시 */}
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
                            {newsList.length > 0 ? (
                                <>
                                    <KeywordButtons newsList={newsList} onSelect={setSelectedNews} />
                                    {selectedNews && <ArticleContent news={selectedNews} />}
                                </>
                            ) : (
                                <p>해당 날짜의 뉴스 데이터가 없습니다.</p>
                            )}
                        </>
                    )}
                </div>
            )}
            <div className="footer">
                <button onClick={handlePrevDate}>이전</button>
                <span>{formatDateToDisplay(currentDate)}</span>
                {!isToday(currentDate) && <button onClick={handleNextDate}>다음</button>}
            </div>
        </div>
    );
};

export default NewsletterPage;
