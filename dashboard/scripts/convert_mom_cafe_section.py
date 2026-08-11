import os
import re

news_dir = "dashboard/news"
html_files = [f for f in os.listdir(news_dir) if f.endswith(".html") and f.startswith("하남감일위례지역뉴스_")]

# We only need to convert files from 20260802 to 20260809
target_files = [f for f in html_files if any(d in f for d in ["20260802", "20260803", "20260804", "20260805", "20260806", "20260807", "20260808", "20260809"])]

num_map = {
    "①": "1️⃣", "②": "2️⃣", "③": "3️⃣",
    "1": "1️⃣", "2": "2️⃣", "3": "3️⃣"
}

for filename in target_files:
    filepath = os.path.join(news_dir, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the mom-cafe section
    mom_cafe_match = re.search(r'(<!-- ===== 섹션 \d+: (?:이번 주 )?맘카페 HOT 이슈 TOP \d+ ===== -->.*?<div id="mom-cafe">.*?)(</div>\s*(?:<!-- 하단 네비게이션 -->|<div class="bottom-nav">|</body>))', content, re.DOTALL)
    if not mom_cafe_match:
        # Fallback search if comments vary
        mom_cafe_match = re.search(r'(<div id="mom-cafe">.*?)(</div>\s*(?:<!-- 하단 네비게이션 -->|<div class="bottom-nav">|</body>))', content, re.DOTALL)

    if mom_cafe_match:
        mom_section = mom_cafe_match.group(1)
        suffix = mom_cafe_match.group(2)
        
        # We need to extract the header block (e.g. section title, paragraph explanation)
        header_part_match = re.search(r'(<div id="mom-cafe">.*?<p>.*?</p>)', mom_section, re.DOTALL)
        if header_part_match:
            header_part = header_part_match.group(1)
        else:
            header_part = '<div id="mom-cafe">\n<div class="section-title pink">💬 하남 맘카페 HOT 이슈 TOP 3</div>'

        # Parse each article-card inside the mom-cafe section
        cards = re.findall(r'<div class="article-card">.*?</div>\s*</div>', mom_section, re.DOTALL)
        if not cards:
            # Try matching without the trailing </div> if it is closed differently
            cards = re.findall(r'<div class="article-card">.*?</div>', mom_section, re.DOTALL)

        new_cards_html = []
        for card in cards:
            # Extract badge (cafe name)
            badge_match = re.search(r'<div class="badge">([^|]+)(?:\|.*?)?</div>', card)
            cafe_name = badge_match.group(1).strip() if badge_match else ""
            
            # Extract title
            title_match = re.search(r'<h3>\s*([①②③\d])\s*(.*?)\s*</h3>', card)
            if title_match:
                num_char = title_match.group(1)
                emoji_num = num_map.get(num_char, "1️⃣")
                title_text = title_match.group(2).strip()
            else:
                emoji_num = "1️⃣"
                title_text = "이슈"

            # Clean title_text if it has trailing parenthesized cafe name already
            title_text = re.sub(r'\s*\([^)]+\)$', '', title_text).strip()

            # Extract fields from the summary paragraph
            # We look for:
            # • 현황/내용: ... or 현황: ...
            # • 핵심 포인트: ... or 포인트: ...
            # • 주민 반응: ... or 반응: ...
            
            summary_match = re.search(r'<div class="summary">(.*?)</div>', card, re.DOTALL)
            summary_content = summary_match.group(1) if summary_match else ""
            
            # Helper to find text by marker
            def find_text(patterns, text):
                for p in patterns:
                    m = re.search(p, text, re.DOTALL)
                    if m:
                        return m.group(1).strip()
                return ""

            status = find_text([r'현황/내용:\s*(.*?)(?:<br|•|<strong>|$)', r'현황:\s*(.*?)(?:<br|•|<strong>|$)'], summary_content)
            # Strip tags and bullet characters
            status = re.sub(r'<[^>]+>', '', status).strip("• ").strip()

            point = find_text([r'핵심 포인트:\s*(.*?)(?:<br|•|<strong>|$)', r'주민 포인트:\s*(.*?)(?:<br|•|<strong>|$)'], summary_content)
            point = re.sub(r'<[^>]+>', '', point).strip("• ").strip()

            reaction = find_text([r'주민 반응:\s*(.*?)(?:<br|•|<strong>|$)', r'반응:\s*(.*?)(?:<br|•|<strong>|$)'], summary_content)
            reaction = re.sub(r'<[^>]+>', '', reaction).strip("• ").strip()

            # Reconstruct in the beautiful mom-issue-card format
            new_card = f"""<div class="mom-issue-card">
<h4>{emoji_num} {title_text} ({cafe_name})</h4>
<div class="mom-detail"><strong>현황:</strong> {status}</div>
<div class="mom-point">💡 주민 포인트: {point}</div>
<div class="mom-reaction">💬 주민 반응: {reaction}</div>
</div>"""
            new_cards_html.append(new_card)

        # Combine header and new cards
        new_mom_section = header_part + "\n" + "\n".join(new_cards_html) + "\n"
        
        # Replace in content
        content = content.replace(mom_section, new_mom_section)
        
        # Clean section-title class to ensure it is pink
        # <div class="section-title"> -> <div class="section-title pink">
        content = content.replace('<div class="section-title">💬 하남 맘카페', '<div class="section-title pink">💬 하남 맘카페')
        content = content.replace('<div class="section-title">🔥 하남 맘카페', '<div class="section-title pink">💬 하남 맘카페')
        content = content.replace('<div class="section-title pink">🔥 하남 맘카페', '<div class="section-title pink">💬 하남 맘카페')

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully converted mom-cafe layout in {filename}")
