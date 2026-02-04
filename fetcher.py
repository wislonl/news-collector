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
    """
    github_token = os.getenv("GITHUB_TOKEN")
    # GitHub API 必须包含 User-Agent
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Tech-Digest-Collector-Bot"
    }
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

    # 1. 历史总榜 (结合 Topic 和关键词搜索，提高覆盖率)
    print("Fetching GitHub Top Agents...")
    top_agents = search_repos("(topic:agent OR topic:ai-agent OR topic:llm-agent OR \"AI Agent\" OR \"LLM Agent\") stars:>1000")
    
    # 2. 快速上升 (30天内创建)
    last_30_days = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    print(f"Fetching Rising GitHub Agents since {last_30_days}...")
    rising_agents = search_repos(f"(topic:agent OR topic:ai-agent OR topic:llm-agent OR \"AI Agent\" OR \"LLM Agent\") created:>{last_30_days}")

    # 如果 rising_agents 太少，尝试放宽条件搜索关键词
    if len(rising_agents) < 5:
        print("Too few rising agents found with topics, trying keyword search...")
        more_rising = search_repos(f"\"AI Agent\" created:>{last_30_days}")
        rising_agents.extend([r for r in more_rising if r['full_name'] not in [x['full_name'] for x in rising_agents]])

    return {
        "top": top_agents,
        "rising": rising_agents
    }

if __name__ == "__main__":
    news = fetch_news()
    print(f"Fetched {len(news['zh'])} Chinese news and {len(news['en'])} English news.")
    
    github_data = fetch_github_agents()
    print(f"Fetched {len(github_data['top'])} Top Agents and {len(github_data['rising'])} Rising Agents.")
