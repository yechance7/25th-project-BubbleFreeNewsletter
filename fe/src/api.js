// fe/api.js
import axios from 'axios';

const API_URL = 'http://localhost:8000';  // FastAPI 서버의 URL

export const searchByTitle = async (query) => {
    try {
        const response = await axios.get(`${API_URL}/search/title/${query}`);
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
