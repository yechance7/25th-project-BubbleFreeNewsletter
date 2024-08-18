import React, { useState } from 'react';
import './MyPage.css';

// 하드코딩된 기사 데이터
const articles = [
    { article_id: '1', title: '광복절 0시에 기미가요 방송한 KBS, 정말 우연인가', content: '해방된 지 80년 가까운 세월이 흘렀는데 아직도 ‘친일’ 프레임이 판치는 현실은 참담하다. 문재인 정부 때 김원웅 당시 광복회장은 “대한민국은 반민족 친일”이라고 매도해 광복절을 두 쪽 냈고, 문 당시 대통령은 이를 방조하며 박수까지 쳤다. 그러던 민주당이 또다시 ‘친일’ 이슈를 들고나와 정권 공격의 소재로 쓰고 광복절을 망치고 있다. 나라가 거꾸로 가고 있다.', logits: [ 3.0557, -3.2385] },
    { article_id: '2', title: '나라 되찾은 광복절에 펼쳐진 기막힌 풍경들', content: '그런데 해방을 기념하는 광복절에, 그것도 윤석열 정부의 노골적 친일 행태에 국민의 신경이 곤두서 있는 때에 굳이 방영하니 고의성을 의심받는 것이다. 강제동원 대법원 판결 무시와 후쿠시마 오염수 방류 협조에 이어, 사도광산 유네스코 문화유산 등재 찬성, 친일파들의 명예를 회복시키겠다는 김형석 독립기념관장 임명 강행에 이르기까지 이 정부의 친일 기조는 확신에 찬 듯 체계적으로 이뤄지고 있다. 최근엔 서울 지하철역 3곳에 설치됐던 독도 조형물이 철거되기도 했다. 이 모든 게 정말 우연인가.', logits: [ -2.7187, 2.0071] },
    { article_id: '3', title: "28년 만의 상속세 개편안 나와도 '현실감' 들지 않는 이유", content: '우리 상속세 체계는 다른 선진국보다 지나치게 과중하다. 그 결과 서울에 아파트 한 채만 가져도 상속세 걱정을 해야 할 지경에 이르렀다. 이것은 상속세의 본뜻이 아니다.', logits: [ 3.1263, -3.2706] },
    { article_id: '4', title: '상속세까지 오기 부리듯 ‘부자감세’, 민심 상처 덧낸다', content: "내수경기 악화에 고통을 겪는 민심을 달래기보다는 ‘부자감세를 완성하겠다’는 의지를 명확히 한 것으로 해석된다. 그런 처지임에도 부자감세를 이렇게 노골적으로 밀고 가는 건 민심은 아랑곳하지 않는 오만, 오기의 국정이 아닐 수 없다.", logits: [-0.6403, -0.2620] },
    // 추가적인 기사들
];

const MyPage = () => {
    const [currentIndex, setCurrentIndex] = useState(0);
    const [selectedOptions, setSelectedOptions] = useState({});
    const [error, setError] = useState(null);
    const userId = 'user1';  // 여기에서 동적으로 또는 실제 사용자 ID를 받아올 수 있습니다.

    const handleSelect = (article_id) => {
        setSelectedOptions(prev => ({
            ...prev,
            [article_id]: { selected: true }
        }));

        if (currentIndex < articles.length - 2) {
            setCurrentIndex(prev => prev + 2);
        } else {
            submitSelections();
        }
    };

    const submitSelections = async () => {
        try {
            const selections = Object.entries(selectedOptions).map(([article_id, { selected }]) => {
                const article = articles.find(article => article.article_id === article_id);
                return {
                    article_id,
                    selected,
                    logits: article.logits
                };
            });

            const response = await fetch('http://127.0.0.1:8000/save-selections', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId, selections })
            });
            
            const result = await response.json();

            alert(`Selections saved successfully! Average logits: ${JSON.stringify(result.average_logits)}`);
        } catch (err) {
            setError('Failed to save selections.');
        }
    };

    const currentArticles = articles.slice(currentIndex, currentIndex + 2);

    return (
        <div className="MyPage">
            {currentArticles.length === 2 ? (
                <div className="articles-container">
                    {currentArticles.map(article => (
                        <div key={article.article_id} className="article-container">
                            <h2>{article.title}</h2>
                            <p>{article.content}</p>
                            <div className="button-group">
                                <button onClick={() => handleSelect(article.article_id)}>Select</button>
                            </div>
                        </div>
                    ))}
                </div>
            ) : (
                <p>No more articles to review.</p>
            )}
            {error && <p className="error">{error}</p>}
        </div>
    );
};

export default MyPage;