import os

news_dir = "dashboard/news"
html_files = [f for f in os.listdir(news_dir) if f.endswith(".html") and f.startswith("하남감일위례지역뉴스_")]

# We want to replace the title. Let's cover multiple variations (spaces, parentheses, with or without icon in heading)
target_variations = [
    "우리동네 국회의원 이광재 의정 소식 (하남갑)",
    "우리동네 국회의원 이광재 의정 소식(하남갑)",
    "우리동네 국회의원 이광재 의정소식 (하남갑)",
    "우리동네 국회의원 이광재 의정소식(하남갑)",
    "우리동네 국회의원 이광재 의정소식(하납갑)",
    "우리동네 국회의원 이광재 의정 소식 (하남갑)",
    "우리동네 국회의원 이광재 의정 소식(하남갑)",
]

replacement = "우리동네 국회의원 이광재 언론보도"

for filename in html_files:
    filepath = os.path.join(news_dir, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    changed = False
    for var in target_variations:
        if var in content:
            content = content.replace(var, replacement)
            changed = True
            
    # Also handle cases where there is an emoji/icon in the heading tag, e.g., 🗣️ 우리동네 국회의원...
    # We want to replace the core text but keep the emoji in the heading if it is there, OR replace it entirely.
    # The request says: 지금 '우리동네 국회의원 이광재 의정소식(하납갑)' 이 제목을 '우리동네 국회의원 이광재 언론보도' 로 수정
    # Let's check if there are matches in the file and replace them.
    
    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated title in {filename}")
    else:
        # Fallback regex search to replace variations
        import re
        content, count = re.subn(r"우리동네\s*국회의원\s*이광재\s*의정\s*소식\s*\(하남갑\)", replacement, content)
        content, count2 = re.subn(r"우리동네\s*국회의원\s*이광재\s*의정소식\s*\(하남갑\)", replacement, content)
        content, count3 = re.subn(r"우리동네\s*국회의원\s*이광재\s*의정소식\s*\(하납갑\)", replacement, content)
        if count + count2 + count3 > 0:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Updated title via regex in {filename}")
