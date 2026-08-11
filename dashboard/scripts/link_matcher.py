import os
import re
import urllib.parse
import requests
from bs4 import BeautifulSoup
import time

NEWS_DIR = r"d:\github\newsletter\newsletter\dashboard\news"

# Map news sources to their domain keywords
DOMAIN_MAP = {
    '조선일보': 'chosun.com',
    '머니투데이': 'mt.co.kr',
    '강원일보': 'kwnews.co.kr',
    '시티뉴스': 'ctnews.co.kr',
    '하남타임즈': 'hanamtimes.com',
    '하남일보': 'hanamilbo',
    '경기일보': 'kyeonggi.com',
    '경인일보': 'kyeongin.com',
    '중부일보': 'joongboo.com',
    '연합뉴스': 'yna.co.kr',
    '서울신문': 'seoul.co.kr',
    '문화일보': 'munhwa.com',
    '인천일보': 'incheonilbo.com',
    '디지털타임스': 'dt.co.kr',
    '국민일보': 'kmib.co.kr',
    '뉴스1': 'news1.kr',
    '뉴시스': 'newsis.com',
    'KBS': 'kbs.co.kr',
    '하남시청': 'hanam.go.kr',
}

def clean_title(title):
    # Remove leading numbers, quotes, and punctuation
    cleaned = re.sub(r'^[①②③④⑤⑥⑦⑧⑨⑩]\s*', '', title)
    cleaned = re.sub(r'[^\w\s]', ' ', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip()

def extract_candidates(soup, source_name):
    candidates = []
    # Find all anchor tags
    for a in soup.find_all("a"):
        href = a.get("href")
        if not href:
            continue
        is_naver = "naver.com" in href
        is_naver_news = "news.naver.com" in href
        if is_naver and not is_naver_news:
            continue
        if href.startswith("/") or href.startswith("?") or href.startswith("#") or href.startswith("javascript:"):
            continue
            
        text = a.text.strip().replace("새 창 열림", "").strip()
        if len(text) < 6:
            continue
            
        # Ignore common boilerplate links
        if text in ["이용약관", "개인정보처리방침", "검색 고객센터", "네이버", "NAVER", "지식iN에 질문하기", "검색 도움말 보기", "© NAVER Corp.", "© NAVER Corp."]:
            continue
            
        classes = a.get("class", [])
        has_fender = any(c.startswith("fender-ui_") for c in classes)
        has_news_tit = "news_tit" in classes
        is_summary_link = any("bIVnnJgbwgo_kQb7" in c for c in classes)
        
        if (has_fender or has_news_tit or not classes) and not is_summary_link:
            if not any(c['link'] == href for c in candidates):
                candidates.append({
                    "title": text,
                    "link": href
                })
    return candidates

def search_naver_news(title, source_name):
    cleaned = clean_title(title)
    words = [w for w in cleaned.split() if len(w) > 1]
    
    # Exclude common noise words from keywords
    noise_words = {'의원', '의원실', '국회의원', '대변', '주민', '입장', '기사', '확인', '보기', '공직자', '특강', '강조', '제안', '구상', '요구', '본격화', '준공', '예정', '재개장', '준비', '완료'}
    keywords = [w for w in words if w not in noise_words]
    if not keywords:
        keywords = words
        
    queries_to_try = []
    # Try searching with targeted keywords
    if len(keywords) >= 3:
        queries_to_try.append(" ".join(keywords[:3]))
        queries_to_try.append(f"{source_name} " + " ".join(keywords[:3]))
    if len(keywords) >= 2:
        queries_to_try.append(" ".join(keywords[:2]))
        queries_to_try.append(f"{source_name} " + " ".join(keywords[:2]))
    queries_to_try.append(cleaned[:50])
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    
    for query in queries_to_try:
        url = "https://search.naver.com/search.naver?where=news&query=" + urllib.parse.quote(query)
        try:
            time.sleep(1) # Be polite
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, "html.parser")
            candidates = extract_candidates(soup, source_name)
            if candidates:
                return candidates, query
        except Exception as e:
            print(f"Error searching for query '{query}': {e}")
            
    return [], ""

def calculate_match_score(target_title, target_source, candidate_title, candidate_link):
    score = 0
    # Clean titles
    t_clean = clean_title(target_title)
    c_clean = clean_title(candidate_title)
    
    t_words = set(t_clean.split())
    c_words = set(c_clean.split())
    
    # Keyword overlap
    overlap = t_words.intersection(c_words)
    score += len(overlap) * 10
    
    # Boost if source domain keyword is in candidate link
    expected_domain = DOMAIN_MAP.get(target_source, "")
    if expected_domain and expected_domain in candidate_link:
        score += 50
        
    # Boost if target source name is in candidate title or page
    if target_source in candidate_title:
        score += 20
        
    return score

def find_best_link(target_title, target_source):
    print(f"Matching: [{target_source}] '{target_title}'")
    candidates, used_query = search_naver_news(target_title, target_source)
    if not candidates:
        print("  -> No candidates found")
        return None
        
    best_candidate = None
    best_score = -1
    
    for c in candidates:
        score = calculate_match_score(target_title, target_source, c['title'], c['link'])
        if score > best_score:
            best_score = score
            best_candidate = c
            
    if best_candidate and best_score >= 30: # Minimum match threshold
        print(f"  -> Found Best Match (Score: {best_score}): {best_candidate['title']} -> {best_candidate['link']}")
        return best_candidate['link']
    else:
        print(f"  -> Match below threshold (Best Score: {best_score}): {best_candidate['title'] if best_candidate else 'None'}")
        return None

def process_html_file(file_path):
    print(f"\nProcessing file: {os.path.basename(file_path)}")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    soup = BeautifulSoup(content, "html.parser")
    updated = False
    
    # Process regular article-cards
    cards = soup.select(".article-card")
    for card in cards:
        # Title
        h3 = card.find("h3")
        if not h3:
            continue
        title = h3.text.strip()
        
        # Source & link
        source_div = card.find("div", class_="source")
        if not source_div:
            continue
            
        a_tag = source_div.find("a")
        if not a_tag:
            continue
            
        current_href = a_tag.get("href")
        
        # Parse source name
        source_text = source_div.text.replace("📌 출처:", "").strip()
        # Source text might be like: "조선일보 | 기사 원문 보기 →"
        source_name = source_text.split("|")[0].strip()
        
        # Search and find best link
        new_link = find_best_link(title, source_name)
        if new_link and new_link != current_href:
            # We will replace in the raw content to preserve formatting
            target_str = f'href="{current_href}"'
            replacement_str = f'href="{new_link}"'
            
            # Locate the card's source div block in HTML string and replace
            # To be safe, let's find the exact a tag in soup and replace it there
            a_tag['href'] = new_link
            updated = True
            
    # Process naver-news list items
    news_list = soup.select(".news-list li")
    for li in news_list:
        strong = li.find("strong")
        if not strong:
            continue
        title = strong.text.strip()
        
        meta_div = li.find("div", class_="news-meta")
        if not meta_div:
            continue
            
        a_tag = meta_div.find("a")
        if not a_tag:
            continue
            
        current_href = a_tag.get("href")
        
        source_text = meta_div.text.replace("📌", "").strip()
        source_name = source_text.split("|")[0].strip()
        
        new_link = find_best_link(title, source_name)
        if new_link and new_link != current_href:
            a_tag['href'] = new_link
            updated = True

    if updated:
        # Write back updated soup
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"Saved changes to {os.path.basename(file_path)}")
    else:
        print("No changes made to this file.")

def main():
    files = [f for f in os.listdir(NEWS_DIR) if f.startswith("하남감일위례지역뉴스_") and f.endswith(".html")]
    # Sort files to process newest first
    files.sort(reverse=True)
    
    for file in files:
        file_path = os.path.join(NEWS_DIR, file)
        process_html_file(file_path)

if __name__ == "__main__":
    main()
