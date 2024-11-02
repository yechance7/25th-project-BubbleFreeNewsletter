// fe/components/ArticleList.js
import React from 'react';

const ArticleList = ({ articles }) => {
    return (
        <div>
            <h2>기사 목록</h2>
            {articles.length > 0 ? (
                <ul>
                    {articles.map(article => (
                        <li key={article.article_id}>
                            <h3>{article.title}</h3>
                            <p><strong>Date:</strong> {article.date}</p>
                            <br />
                            <p>{article.content}</p>
                            {/* <p><strong>Keyword:</strong> {article.keyword}</p> */}
                        </li>
                    ))}
                </ul>
            ) : (
                <p>0개의 기사가 검색되었습니다.</p>
            )}
        </div>
    );
};

export default ArticleList;
