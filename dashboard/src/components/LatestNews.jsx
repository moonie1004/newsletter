import React from 'react';

const LatestNews = ({ newsData, onReadMore }) => {
  // Get latest 3 days
  const latestNews = newsData.slice(0, 3);

  return (
    <div className="latest-news">
      <h2 className="section-title">🕒 최근 하남 뉴스</h2>
      <div className="news-list">
        {latestNews.map((dayNews, index) => (
          <div key={index} className="glass-card news-item">
            <span className="news-date">{dayNews.date}</span>
            {dayNews.mainNews.length > 0 ? (
              <>
                <h3>{dayNews.mainNews[0].title}</h3>
                <p>{dayNews.mainNews[0].summary.substring(0, 150)}...</p>
              </>
            ) : (
              <p>주요 뉴스가 없습니다.</p>
            )}
            <a className="read-more" onClick={(e) => { e.preventDefault(); onReadMore(dayNews); }}>
              자세히 보기 &rarr;
            </a>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LatestNews;
