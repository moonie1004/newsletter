import React, { useState } from 'react';
import { format, addMonths, subMonths, startOfMonth, endOfMonth, startOfWeek, endOfWeek, isSameMonth, isSameDay, addDays, parseISO } from 'date-fns';

const CalendarView = ({ newsData, onDateSelect, selectedNews }) => {
  const [currentDate, setCurrentDate] = useState(new Date());
  
  // Extract all available news dates
  const availableDates = newsData.map(news => news.date); // e.g. "2026-08-03"

  const nextMonth = () => setCurrentDate(addMonths(currentDate, 1));
  const prevMonth = () => setCurrentDate(subMonths(currentDate, 1));

  const monthStart = startOfMonth(currentDate);
  const monthEnd = endOfMonth(monthStart);
  const startDate = startOfWeek(monthStart);
  const endDate = endOfWeek(monthEnd);

  const renderDays = () => {
    const days = [];
    const date = ['일', '월', '화', '수', '목', '금', '토'];
    for (let i = 0; i < 7; i++) {
      days.push(
        <div className="calendar-day-header" key={i}>
          {date[i]}
        </div>
      );
    }
    return <div className="calendar-grid">{days}</div>;
  };

  const renderCells = () => {
    const rows = [];
    let days = [];
    let day = startDate;
    let formattedDate = '';

    while (day <= endDate) {
      for (let i = 0; i < 7; i++) {
        formattedDate = format(day, 'd');
        const dayKey = format(day, 'yyyy-MM-dd');
        
        const hasNews = availableDates.includes(dayKey);
        const isCurrentMonth = isSameMonth(day, monthStart);
        const isSelected = selectedNews && selectedNews.date === dayKey;
        
        days.push(
          <div
            className={`calendar-cell ${!isCurrentMonth ? 'empty' : ''} ${hasNews ? 'has-news' : ''} ${isSelected ? 'selected' : ''}`}
            key={day}
            onClick={() => {
              if (hasNews) {
                const newsItem = newsData.find(n => n.date === dayKey);
                onDateSelect(newsItem);
              }
            }}
            title={hasNews ? "뉴스 보기" : ""}
          >
            {isCurrentMonth ? formattedDate : ''}
          </div>
        );
        day = addDays(day, 1);
      }
      rows.push(
        <div className="calendar-grid" key={day}>
          {days}
        </div>
      );
      days = [];
    }
    return <div>{rows}</div>;
  };

  return (
    <div className="calendar-wrapper glass-card">
      <h2 className="section-title">📅 월별 뉴스 보기</h2>
      
      <div className="calendar-header">
        <button onClick={prevMonth} className="calendar-nav-btn">&lt;</button>
        <div style={{ fontWeight: 'bold', fontSize: '1.2rem', color: 'var(--text-main)' }}>
          {format(currentDate, 'yyyy년 M월')}
        </div>
        <button onClick={nextMonth} className="calendar-nav-btn">&gt;</button>
      </div>
      
      {renderDays()}
      {renderCells()}
      
      <p style={{ marginTop: '20px', fontSize: '0.85rem', color: 'var(--text-muted)', textAlign: 'center' }}>
        * 파란색으로 표시된 날짜를 클릭하면 해당 일자의 뉴스레터를 확인할 수 있습니다.
      </p>
    </div>
  );
};

export default CalendarView;
