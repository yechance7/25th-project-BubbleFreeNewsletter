// fe/components/SearchBar.js
import React, { useState, useEffect } from 'react';  // useEffect도 추가해야 함
import { searchByTitle, searchByKeyword } from '../api';
import ArticleList from './ArticleList';

const SearchBar = () => {
    const [query, setQuery] = useState('');
    const [searchType, setSearchType] = useState('title');
    const [articles, setArticles] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        console.log(articles);  // articles 배열이 제대로 업데이트되는지 확인
    }, [articles]);
    

    const handleSearch = async () => {
        setLoading(true);
        try {
            let results;
            if (searchType === 'title') {
                results = await searchByTitle(query);
            } else {
                results = await searchByKeyword(query);
            }
            setArticles(results);
        } catch (error) {
            console.error('Error searching articles:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h1>Article Search</h1>
            <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Enter search query"
            />
            <select value={searchType} onChange={(e) => setSearchType(e.target.value)}>
                <option value="title">Title</option>
                <option value="keyword">Keyword</option>
            </select>
            <button onClick={handleSearch} disabled={loading}>
                {loading ? 'Searching...' : 'Search'}
            </button>
            <ArticleList articles={articles} />
        </div>
    );
};

export default SearchBar;
