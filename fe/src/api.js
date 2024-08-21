// fe/api.js
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';  // FastAPI 서버의 URL

export const searchByTitle = async (query, limit = 4, offset = 0) => {
    try {
        const response = await axios.get(`${API_URL}/search/title`, {
            params: { query, limit, offset }
        });
        return response.data;
    } catch (error) {
        console.error('Error fetching articles by title:', error);
        throw error;
    }
};

export const searchByKeyword = async (query) => {
    try {
        const response = await axios.get(`${API_URL}/search/keyword/${query}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching articles by keyword:', error);
        throw error;
    }
};

export const getArticle = async (articleId) => {
    try {
        const response = await axios.get(`${API_URL}/article/${articleId}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching article by ID:', error);
        throw error;
    }
};


export const fetchUserData = async (userId) => {
    try {
        const response = await axios.get(`${API_URL}/user_info/${userId}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching user data:', error);
        throw error;
    }
};

export const fetchTodayNewsList = async (userId) => {
    try {
        const response = await axios.get(`${API_URL}/todayNewsList/${userId}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching today\'s news list:', error);
        throw error;
    }
};