import React from 'react';

const ArticleContent = ({ news }) => {
    return (
        <div style={styles.container}>
            <h2 style={styles.title}>{news.title}</h2>
            <div style={styles.spacer}></div>
            {news.image && (
                <img 
                    src={news.image}
                    alt="News Image" 
                    style={styles.image}
                />
            )}
            <hr style={styles.hr} />
            <p style={styles.content}>{news.content}</p>
        </div>
    );
};


const styles = {
    container: {
        fontFamily: '"Arial", sans-serif',
        color: '#333',
        lineHeight: '1.6',
        maxWidth: '700px',
        margin: '0 auto',
        padding: '20px',
        backgroundColor: '#f9f9f9',
        borderRadius: '8px',
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
    },
    title: {
        fontSize: '24px',
        fontWeight: 'bold',
        color: '#2c3e50',
        marginBottom: '10px',
    },
    spacer: {
        height: '20px', // 제목과 이미지 사이에 간격을 추가
    },
    image: {
        width: '100%',        
        height: 'auto',        
        maxWidth: '600px',   
        maxHeight: '400px',   
        objectFit: 'cover',    
        borderRadius: '8px',
        boxShadow: '0 2px 4px rgba(0, 0, 0, 0.2)',
    },
    hr: {
        margin: '20px 0',
        border: '0',
        height: '1px',
        backgroundColor: '#ddd',
    },
    content: {
        fontSize: '16px',
        lineHeight: '1.8',
        textAlign: 'justify',
    }
};

export default ArticleContent;
