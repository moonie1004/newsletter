import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const NEWSLETTER_DIR = path.join(__dirname, '../../');
const OUTPUT_FILE = path.join(__dirname, '../public/newsData.json');

function parseMarkdown(content, dateStr) {
  const data = {
    date: dateStr, // e.g. "2026-08-03"
    mainNews: [],
    top5: [],
    cafeIssues: [],
    cultureEvents: []
  };

  const lines = content.split('\n');
  let currentSection = '';
  let currentNews = null;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();

    if (line.startsWith('## 📌 주요 지역 현안')) {
      currentSection = 'mainNews';
      continue;
    } else if (line.startsWith('## 📰 네이버 검색 상위')) {
      currentSection = 'top5';
      continue;
    } else if (line.startsWith('## ☕ 하남지역 네이버 카페')) {
      currentSection = 'cafeIssues';
      continue;
    } else if (line.startsWith('## 🎭 하남지역 주요 문화행사')) {
      currentSection = 'cultureEvents';
      continue;
    }

    if (currentSection === 'mainNews') {
      if (line.startsWith('### ')) {
        if (currentNews) {
          data.mainNews.push(currentNews);
        }
        currentNews = { title: line.replace(/^###\s*\d+\.\s*/, '').trim(), summary: '', source: '', link: '' };
      } else if (line.startsWith('> **주요 내용 요약 초안') || line.startsWith('> **주요 내용 요약')) {
        currentNews.summary = line.replace(/^>\s*\*\*.*?\*\*\s*/, '').trim();
      } else if (line.startsWith('- **📌 출처:**')) {
        const sourceLine = line.replace('- **📌 출처:**', '').trim();
        // Extract link if exists: source | [원문 기사 확인](URL)
        const match = sourceLine.match(/^(.*?)\|\s*\[.*?\]\((.*?)\)$/);
        if (match) {
          currentNews.source = match[1].trim();
          currentNews.link = match[2].trim();
        } else {
          const simpleMatch = sourceLine.match(/^(.*?)\s*\|\s*(.*?)$/);
          if (simpleMatch) {
            currentNews.source = simpleMatch[1].trim();
            // sometimes it's text like 원문 기사 확인(추후 보완)
          } else {
            currentNews.source = sourceLine;
          }
        }
      }
    } else if (currentSection === 'top5') {
      if (line.match(/^\d+\.\s/)) {
        data.top5.push(line.replace(/^\d+\.\s\*\*(.*?)\*\*\s*-\s*(.*)$/, (m, p1, p2) => `${p1} - ${p2}`).replace(/^\d+\.\s/, ''));
      }
    } else if (currentSection === 'cafeIssues') {
      if (line.startsWith('- **')) {
        data.cafeIssues.push(line.replace(/^- \*\*(.*?)\*\*\s*(.*)$/, (m, p1, p2) => `${p1} ${p2}`));
      }
    } else if (currentSection === 'cultureEvents') {
      if (line.startsWith('- **')) {
        data.cultureEvents.push(line.replace(/^- \*\*(.*?)\*\*\s*(.*)$/, (m, p1, p2) => `${p1} ${p2}`));
      }
    }
  }

  if (currentNews) {
    data.mainNews.push(currentNews);
  }

  return data;
}

function generateData() {
  const files = fs.readdirSync(NEWSLETTER_DIR);
  const newsFiles = files.filter(f => f.startsWith('하남지역뉴스_') && f.endsWith('.md') && !f.includes('매일발행'));
  
  const allData = [];

  for (const file of newsFiles) {
    // 하남지역뉴스_20260803.md -> 20260803
    const match = file.match(/하남지역뉴스_(\d{8})\.md/);
    if (!match) continue;

    const dateRaw = match[1];
    const dateStr = `${dateRaw.substring(0,4)}-${dateRaw.substring(4,6)}-${dateRaw.substring(6,8)}`;
    
    const content = fs.readFileSync(path.join(NEWSLETTER_DIR, file), 'utf-8');
    const parsedData = parseMarkdown(content, dateStr);
    allData.push(parsedData);
  }

  // Sort by date descending
  allData.sort((a, b) => b.date.localeCompare(a.date));

  fs.writeFileSync(OUTPUT_FILE, JSON.stringify(allData, null, 2));
  console.log(`Generated newsData.json with ${allData.length} records.`);
}

generateData();
