import React, { useState } from 'react';
import './MyPage.css';

// 하드코딩된 기사 데이터
const articles = [
    { article_id: '1', 
        title: '광복절 0시에 기미가요 방송한 KBS, 정말 우연인가', 
        content: '해방된 지 80년 가까운 세월이 흘렀는데 아직도 ‘친일’ 프레임이 판치는 현실은 참담하다. 문재인 정부 때 김원웅 당시 광복회장은 “대한민국은 반민족 친일”이라고 매도해 광복절을 두 쪽 냈고, 문 당시 대통령은 이를 방조하며 박수까지 쳤다. 그러던 민주당이 또다시 ‘친일’ 이슈를 들고나와 정권 공격의 소재로 쓰고 광복절을 망치고 있다. 나라가 거꾸로 가고 있다.', 
        logits: [ 3.0557, -3.2385],
    image_url: 'https://flexible.img.hani.co.kr/flexible/normal/923/550/imgdb/original/2024/0815/20240815502810.jpg'},
    { article_id: '2', 
        title: '나라 되찾은 광복절에 펼쳐진 기막힌 풍경들', 
        content: '그런데 해방을 기념하는 광복절에, 그것도 윤석열 정부의 노골적 친일 행태에 국민의 신경이 곤두서 있는 때에 굳이 방영하니 고의성을 의심받는 것이다. 강제동원 대법원 판결 무시와 후쿠시마 오염수 방류 협조에 이어, 사도광산 유네스코 문화유산 등재 찬성, 친일파들의 명예를 회복시키겠다는 김형석 독립기념관장 임명 강행에 이르기까지 이 정부의 친일 기조는 확신에 찬 듯 체계적으로 이뤄지고 있다. 최근엔 서울 지하철역 3곳에 설치됐던 독도 조형물이 철거되기도 했다. 이 모든 게 정말 우연인가.', 
        logits: [ -2.7187, 2.0071],
        image_url: 'https://www.chosun.com/resizer/v2/UJSKFM3IBZAMDLKGDKXMDXRX4A.JPG?auth=f0baf0de2b4d061aec30300f4cf654c7e9fc75095ce47a3ce5b0451cabaec7c2&width=616' },
    { article_id: '3', 
        title: "28년 만의 상속세 개편안 나와도 '현실감' 들지 않는 이유", 
        content: '우리 상속세 체계는 다른 선진국보다 지나치게 과중하다. 그 결과 서울에 아파트 한 채만 가져도 상속세 걱정을 해야 할 지경에 이르렀다. 이것은 상속세의 본뜻이 아니다.', 
        logits: [ 3.1263, -3.2706],
        image_url: 'https://www.chosun.com/resizer/v2/UTPRD4GSWJYHMD5OJCOED5WIRQ.jpg?auth=d8d9fc58983280c88c52aee6886a5e0821c7acd2f90e472e524cb0df69ddb608&width=616'},
    { article_id: '4', 
        title: '상속세까지 오기 부리듯 ‘부자감세’, 민심 상처 덧낸다', 
        content: "내수경기 악화에 고통을 겪는 민심을 달래기보다는 ‘부자감세를 완성하겠다’는 의지를 명확히 한 것으로 해석된다. 그런 처지임에도 부자감세를 이렇게 노골적으로 밀고 가는 건 민심은 아랑곳하지 않는 오만, 오기의 국정이 아닐 수 없다.", 
        logits: [-0.6403, -0.2620],
        image_url: 'https://flexible.img.hani.co.kr/flexible/normal/970/665/imgdb/original/2024/0725/20240725503649.jpg'  },
    { article_id: '5', 
        title: '이재명 2기 체제, 당내 민주주의와 협치 주도가 최대 과제', 
        content: "이 대표 2기 체제 민주당의 가장 큰 과제는 민생과 개혁이다. 국회 과반 의석을 점한 정당으로서 당면한 민생·경제 위기를 극복할 해법을 능동적으로 내놓고, 연금개혁·기후위기·지방소멸 등 국가적 의제의 대안도 책임 있게 제시해야 한다. 윤석열 정부의 권력 사유화, 방송장악, 뉴라이트식 역사 뒤집기 같은 퇴행에 단호하게 맞서야 함은 물론이다.", 
        logits: [-0.7666, -0.1259],
        image_url: 'https://img.khan.co.kr/news/2024/08/18/news-p.v1.20240818.b783d6fd1f474f70b813149ddd6795eb_P1.webp' },
    { article_id: '6', 
        title: '‘친명만의 리그’로 연임 성공한 이재명 대표의 과제', 
        content: "이 대표가 압승을 즐길 입장도 아니다. 권리당원 투표율(42.18%)이 과반을 넘기지 못하며 저조한 수준에 머물렀다. 특히 보수 강세인 대구·경북의 온라인 투표율(52.24%)이 1위인 반면, 당 텃밭인 호남은 20%대로 하위권에 머무른 게 주목된다. ‘친명 독식’ 일색인 전당대회에 거부감을 품은 전통적인 당 지지층은 등을 돌리고, 소수 강성 지지층만 투표에 열을 올린 정황이 뚜렷하다.", 
        logits: [ 0.2735, -1.3250],
        image_url: 'https://static.vecteezy.com/system/resources/thumbnails/022/059/000/small/no-image-available-icon-vector.jpg'},
    { article_id: '7', 
        title: '경축식 파행에 아쉬움 남긴 통일 독트린…씁쓸했던 광복절', 
        content: "윤 대통령의 언급대로 남북이 자유민주주의 체제로 통일국가가 돼야 완전한 광복이 실현된다는 점, 세계 최악의 수준인 북한 인권이 조속히 개선돼야 한다는 점에는 이견이 있을 수 없다.", 
        logits: [ 2.3514, -2.8987],
        image_url: 'https://static.vecteezy.com/system/resources/thumbnails/022/059/000/small/no-image-available-icon-vector.jpg'},
    { article_id: '8', 
        title: '“자유 통일” 외친 윤 대통령, ‘적대국 남북’ 해소가 먼저다 ', 
        content: "그와 달리 윤 대통령은 북한 체제 붕괴를 전제하고, 남한 주도의 흡수 통일을 노골화했다. 북한 정권의 변화를 기대할 수 없으니 당국과 주민을 분리해서 접근하겠다는 발상도 비현실적이다. 그래놓고 남북 간 대화협의체를 제안했는데, 북한이 응하겠는가.", 
        logits: [-0.6228, -0.2524],
        image_url: 'https://img.khan.co.kr/news/2024/08/15/rcv.YNA.20240815.PYH2024081502460001300_P1.webp' },
        
    
    // 추가적인 기사들
];

const MyPage = () => {
    const [currentIndex, setCurrentIndex] = useState(0);
    const [selectedOptions, setSelectedOptions] = useState({});
    const [nickname, setNickname] = useState('');
    const [error, setError] = useState(null);
    const [expandedArticles, setExpandedArticles] = useState({});

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

    const toggleExpand = (article_id) => {
        setExpandedArticles(prev => ({
            ...prev,
            [article_id]: !prev[article_id]
        }));
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
                body: JSON.stringify({ user_id: nickname, selections })
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
            <div className="nickname-container">
                <h2>닉네임을 입력하세요</h2>
                <input
                    type="text"
                    value={nickname}
                    onChange={(e) => setNickname(e.target.value)}
                    placeholder="닉네임 입력"
                />
            </div>

            {currentArticles.length === 2 ? (
                <div className="articles-container">
                    {currentArticles.map(article => {
                        const isExpanded = expandedArticles[article.article_id];
                        const displayedContent = isExpanded ? article.content : article.content.slice(0, 100);

                        return (
                            <div key={article.article_id} className="article-container">
                                {/* 이미지 추가 */}
                                <img src={article.image_url} alt={article.title} className="article-image" />
                                <h2>{article.title}</h2>
                                <p>{displayedContent}{!isExpanded && article.content.length > 100 && '...'}</p>
                                {article.content.length > 100 && (
                                    <button className="button-small" onClick={() => toggleExpand(article.article_id)}>
                                        {isExpanded ? '접기' : '더보기'}
                                    </button>
                                )}
                                <div className="button-group">
                                    <button onClick={() => handleSelect(article.article_id)}>Select</button>
                                </div>
                            </div>
                        );
                    })}
                </div>
            ) : (
                <p>No more articles to review.</p>
            )}

            {error && <p className="error">{error}</p>}
        </div>
    );
};


export default MyPage;