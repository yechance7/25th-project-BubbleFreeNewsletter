// fe/components/ArticleList.js
import React from 'react';

const ArticleList = ({ articles }) => {
    return (
        <div>
            <h2>Article List</h2>
            {articles.length > 0 ? (
                <ul>
                    {articles.map(article => (
                        <li key={article.article_id}>
                            <h3>{article.title}</h3>
                            <p>{article.content}</p>
                            <p><strong>Keyword:</strong> {article.keyword}</p>
                            <p><strong>Date:</strong> {article.date}</p>
                        </li>
                    ))}
                </ul>
            ) : (
                <p>No articles found</p>
            )}
        </div>
    );
};

export default ArticleList;
