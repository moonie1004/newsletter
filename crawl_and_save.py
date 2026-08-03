import os
import json
import datetime
from dotenv import load_dotenv
from supabase import create_client, Client
import google.generativeai as genai

# 환경변수 불러오기
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Supabase 및 Gemini 초기화
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def summarize_news(content):
    """Gemini API를 사용하여 뉴스를 300자로 요약하고 공손한 어조로 변경합니다."""
    prompt = f"""
    당신은 국회의원실의 핵심 보좌관입니다. 
    다음 뉴스 기사 또는 내용을 공백 포함 약 300자 분량으로 요약해주세요.
    반드시 '~습니다', '~합니다' 등 격식 있고 정중한 보고 어조를 사용하세요.

    [원문 내용]
    {content}
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini API 오류: {e}")
        return "요약에 실패했습니다."

def fetch_and_save_news():
    """크롤링 및 DB 저장 메인 로직"""
    today = datetime.date.today().isoformat()
    
    # -----------------------------------------------------------------
    # 여기에 실제 뉴스 사이트(네이버 뉴스, 하남일보 등) 크롤링 코드가 들어갑니다.
    # 예시(더미 데이터)를 DB에 넣는 로직으로 뼈대를 잡습니다.
    # 실제 적용 시 BeautifulSoup이나 Selenium을 사용해 원문을 가져와야 합니다.
    # -----------------------------------------------------------------
    
    print(f"[{today}] 뉴스 크롤링을 시작합니다...")
    
    # 예시 데이터 1: 주요 지역 현안 (mainNews)
    sample_news_text = "하남시에서 새로운 지하철 9호선 연장 사업을 본격적으로 추진한다고 밝혔습니다. 이번 연장 사업을 통해 지역 주민들의 교통 편의성이 크게 향상될 것으로 기대됩니다. 주요 역사는 미사강변도시를 통과할 예정입니다."
    
    print("AI 요약 진행 중...")
    summary = summarize_news(sample_news_text)
    
    article = {
        "date": today,
        "category": "mainNews",
        "title": "하남시, 9호선 연장 사업 본격 추진",
        "summary": summary,
        "source": "하남일보",
        "link": "https://example.com/news/1"
    }

    # DB에 저장 (Insert)
    print("Supabase DB에 저장 중...")
    try:
        data, count = supabase.table('news_articles').insert(article).execute()
        print("✅ 성공적으로 DB에 저장되었습니다!")
    except Exception as e:
        print(f"❌ DB 저장 실패: {e}")

if __name__ == "__main__":
    fetch_and_save_news()
