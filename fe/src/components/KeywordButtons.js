// src/components/KeywordButtons.js
import React from 'react';

const KeywordButtons = ({ newsList, onSelect }) => {
    return (
        <div>
            {newsList.map((news, index) => (
                <button key={index} onClick={() => onSelect(news)}>
                    {news.keyword.split(',')[0]}
                </button>
            ))}
        </div>
    );
};

export default KeywordButtons;
