import feedparser
import requests
import os
from datetime import datetime, timedelta
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

def fetch_github_agents():
    """
    获取 GitHub 上热门的 Agent/Model 项目
    1. 历史总榜 Top 50 (topic:agent OR topic:ai-agent)
    2. 快速上升 Top 50 (过去 30 天内创建)
    """
    github_token = os.getenv("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github.v3+json"}
    if github_token:
        headers["Authorization"] = f"token {github_token}"
    
    def search_repos(query, sort="stars", order="desc", per_page=50):
        url = f"https://api.github.com/search/repositories?q={query}&sort={sort}&order={order}&per_page={per_page}"
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json().get("items", [])
            else:
                print(f"GitHub API Error: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            print(f"Error searching GitHub: {e}")
            return []

    # 1. 历史总榜
    print("Fetching GitHub Top Agents...")
    top_agents = search_repos("topic:agent+OR+topic:ai-agent+OR+topic:llm-agent")
    
    # 2. 快速上升 (30天内创建且 stars 最多)
    last_30_days = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    print("Fetching Rising GitHub Agents...")
    rising_agents = search_repos(f"topic:agent+OR+topic:ai-agent+OR+topic:llm-agent+created:>{last_30_days}")

    return {
        "top": top_agents,
        "rising": rising_agents
    }

if __name__ == "__main__":
    news = fetch_news()
    print(f"Fetched {len(news['zh'])} Chinese news and {len(news['en'])} English news.")
    
    github_data = fetch_github_agents()
    print(f"Fetched {len(github_data['top'])} Top Agents and {len(github_data['rising'])} Rising Agents.")
