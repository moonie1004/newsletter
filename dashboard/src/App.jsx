import React, { useState, useEffect } from 'react';
import './index.css';
import LatestNews from './components/LatestNews';
import CalendarView from './components/CalendarView';
import NewsModal from './components/NewsModal';

function App() {
  const [newsData, setNewsData] = useState([]);
  const [selectedNews, setSelectedNews] = useState(null);
  const [showCalendar, setShowCalendar] = useState(false);

  useEffect(() => {
    fetch('/newsData.json')
      .then(res => res.json())
      .then(data => {
        setNewsData(data);
      })
      .catch(err => console.error("Failed to load news data", err));
  }, []);

  const handleReadMore = (newsItem) => {
    setSelectedNews(newsItem);
  };

  const closeModal = () => {
    setSelectedNews(null);
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>하남갑뉴스레터</h1>
        <p>매일 업데이트되는 하남시 주요 뉴스 및 시정 소식을 한눈에 확인하세요.</p>
      </header>

      <div className="main-content" style={{ display: 'block', maxWidth: '800px', margin: '0 auto' }}>
        <LatestNews newsData={newsData} onReadMore={handleReadMore} />
        
        <div style={{ textAlign: 'center', marginTop: '50px', paddingBottom: '30px' }}>
          <button 
            className="read-more" 
            onClick={() => setShowCalendar(true)}
            style={{ fontSize: '1.2rem', padding: '16px 40px', borderRadius: '9999px', boxShadow: '0 10px 25px rgba(99, 102, 241, 0.4)' }}
          >
            📅 월별 뉴스 달력으로 보기
          </button>
        </div>
      </div>

      {showCalendar && (
        <div className="modal-overlay" onClick={() => setShowCalendar(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()} style={{ maxWidth: '500px' }}>
            <button className="close-btn" onClick={() => setShowCalendar(false)}>&times;</button>
            <CalendarView 
              newsData={newsData} 
              onDateSelect={(newsItem) => {
                setShowCalendar(false); // 달력 닫기
                handleReadMore(newsItem); // 뉴스 모달 열기
              }} 
              selectedNews={selectedNews} 
            />
          </div>
        </div>
      )}

      {selectedNews && (
        <NewsModal news={selectedNews} onClose={closeModal} />
      )}
    </div>
  );
}

export default App;
