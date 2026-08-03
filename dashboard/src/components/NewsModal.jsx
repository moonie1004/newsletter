import React from 'react';

const NewsModal = ({ news, onClose }) => {
  if (!news) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <button className="close-btn" onClick={onClose}>&times;</button>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <span className="news-date" style={{ marginBottom: 0 }}>{news.date}</span>
          <h2 style={{ fontSize: '1.8rem', color: 'var(--primary-color)', fontWeight: '900', letterSpacing: '-0.5px' }}>하남갑 지역 뉴스레터</h2>
        </div>
        
        {news.mainNews && news.mainNews.length > 0 && (
          <div style={{ marginTop: '20px' }}>
            <h3 style={{ fontSize: '1.2rem', marginBottom: '15px', color: 'var(--text-main)', borderBottom: '2px solid #e2e8f0', paddingBottom: '5px' }}>
              📌 주요 지역 현안
            </h3>
            {news.mainNews.map((item, idx) => (
              <div key={idx} style={{ marginBottom: '25px' }}>
                <h4 className="modal-news-title">{idx + 1}. {item.title}</h4>
                <div className="modal-news-summary">{item.summary}</div>
                <div className="modal-source">
                  <strong>출처:</strong> {item.source} 
                  {item.link && (
                    <span> | <a href={item.link} target="_blank" rel="noreferrer" style={{ color: 'var(--primary-color)', textDecoration: 'none' }}>원문 기사 확인</a></span>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}

        {news.top5 && news.top5.length > 0 && (
          <div style={{ marginTop: '30px' }}>
            <h3 style={{ fontSize: '1.15rem', color: '#ffffff', background: '#03c75a', padding: '10px 18px', borderRadius: '10px', display: 'inline-block', fontWeight: '800', boxShadow: '0 4px 10px rgba(3, 199, 90, 0.3)' }}>
              📰 네이버 검색 상위 뉴스 (Top 5)
            </h3>
            <ol className="top5-list">
              {news.top5.map((item, idx) => (
                <li key={idx} dangerouslySetInnerHTML={{ __html: item }} />
              ))}
            </ol>
          </div>
        )}

        {news.cafeIssues && news.cafeIssues.length > 0 && (
          <div style={{ marginTop: '30px' }}>
            <h3 style={{ fontSize: '1.15rem', color: '#ffffff', background: '#84cc16', padding: '10px 18px', borderRadius: '10px', display: 'inline-block', fontWeight: '800', boxShadow: '0 4px 10px rgba(132, 204, 22, 0.3)' }}>
              ☕ 지역 네이버 카페 주간 이슈
            </h3>
            <ul className="cafe-list">
              {news.cafeIssues.map((item, idx) => (
                <li key={idx} dangerouslySetInnerHTML={{ __html: item }} />
              ))}
            </ul>
          </div>
        )}

        {news.cultureEvents && news.cultureEvents.length > 0 && (
          <div style={{ marginTop: '30px' }}>
            <h3 style={{ fontSize: '1.15rem', color: '#ffffff', background: '#8b5cf6', padding: '10px 18px', borderRadius: '10px', display: 'inline-block', fontWeight: '800', boxShadow: '0 4px 10px rgba(139, 92, 246, 0.3)' }}>
              🎭 지역 주요 문화행사
            </h3>
            <ul className="culture-list">
              {news.cultureEvents.map((item, idx) => (
                <li key={idx} dangerouslySetInnerHTML={{ __html: item }} />
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default NewsModal;
