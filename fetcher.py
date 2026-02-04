import feedparser
from config import NEWS_SOURCES, NEWS_PER_SOURCE

def fetch_news():
    """
    抓取国内外科技新闻
    """
    all_news = {"zh": [], "en": []}
    
    for lang, urls in NEWS_SOURCES.items():
        for url in urls:
            try:
                feed = feedparser.parse(url)
                # 选取每个源的前几条
                entries = feed.entries[:NEWS_PER_SOURCE]
                for entry in entries:
                    all_news[lang].append({
                        "title": entry.title,
                        "link": entry.link,
                        "summary": entry.get("summary", ""),
                        "source": feed.feed.get("title", url),
                        "lang": lang
                    })
            except Exception as e:
                print(f"Error fetching {url}: {e}")
                
    return all_news

if __name__ == "__main__":
    news = fetch_news()
    print(f"Fetched {len(news['zh'])} Chinese news and {len(news['en'])} English news.")
