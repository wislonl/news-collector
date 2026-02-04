from fetcher import fetch_news, fetch_github_agents
from processor import select_top_news, process_news, process_github_repos
from mailer import send_email
import time

def main():
    print("Step 1: Fetching news and GitHub Agent data...")
    raw_news = fetch_news()
    github_data = fetch_github_agents()
    print(f"Fetched {len(raw_news.get('zh', [])) + len(raw_news.get('en', []))} raw news items.")
    print(f"Fetched {len(github_data.get('top', []))} top repos and {len(github_data.get('rising', []))} rising repos.")
    
    print("Step 2: Selecting Top 20 news and processing GitHub repos with AI...")
    top_news = select_top_news(raw_news, count=20)
    print(f"Selected {len(top_news)} top news items.")
    
    # 并行思想（逻辑上）：处理新闻和处理 GitHub 仓库
    print(f"Step 3: Generating summaries for {len(top_news)} news items...")
    processed_news = process_news(top_news)
    print(f"Processed {len(processed_news)} news items.")
    
    print("Step 4: Analyzing GitHub repositories...")
    processed_repos = process_github_repos(github_data)
    print(f"Processed {len(processed_repos.get('top', []))} top repos and {len(processed_repos.get('rising', []))} rising repos.")
    
    print("Step 5: Sending comprehensive daily email...")
    send_email(processed_news, processed_repos)
    
    print("Daily task completed successfully!")

if __name__ == "__main__":
    main()
