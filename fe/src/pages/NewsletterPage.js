// src/pages/NewsletterPage.js
import React, { useState } from 'react';
import { fetchUserData, fetchTodayNewsList } from '../api';
import KeywordButtons from '../components/KeywordButtons';
import ArticleContent from '../components/ArticleContent';

const NewsletterPage = () => {
    const [userId, setUserId] = useState('');
    const [userData, setUserData] = useState(null);
    const [newsList, setNewsList] = useState([]);
    const [selectedNews, setSelectedNews] = useState('');

    const handleUserIdSubmit = async () => {
        try {
            const data = await fetchUserData(userId);
            setUserData(data);
            const news = await fetchTodayNewsList(userId);
            setNewsList(news);
        } catch (error) {
            console.error('Error fetching user data or news list:', error);
        }
    };

    return (
        <div>
            {!userData ? (
                <div>
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
                <div>
                    <h1>BubblePOP NewsLetter 📰</h1>
                    <KeywordButtons newsList={newsList} onSelect={setSelectedNews} />
                    {selectedNews && <ArticleContent news={selectedNews} />}
                </div>
            )}
        </div>
    );
};

export default NewsletterPage;
