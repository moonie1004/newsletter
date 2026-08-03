-- 테이블 삭제 (초기화용, 만약 이미 있다면 삭제)
DROP TABLE IF EXISTS public.news_articles;

-- 테이블 생성
CREATE TABLE public.news_articles (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  date DATE NOT NULL,
  category TEXT NOT NULL,
  title TEXT NOT NULL,
  summary TEXT,
  source TEXT,
  link TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 인덱스 생성 (날짜별 조회를 빠르게 하기 위해)
CREATE INDEX idx_news_articles_date ON public.news_articles(date);
CREATE INDEX idx_news_articles_category ON public.news_articles(category);

-- RLS (Row Level Security) 설정
-- 웹사이트(방문자)는 데이터 읽기만 가능하게 하고, 쓰기/수정은 불가능하게 만듭니다.
ALTER TABLE public.news_articles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read access"
ON public.news_articles
FOR SELECT
TO public
USING (true);

-- (서비스 역할(크롤러)은 기본적으로 RLS를 우회하여 모든 권한을 가집니다)
