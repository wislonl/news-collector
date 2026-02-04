from fetcher import fetch_news, fetch_github_agents
from processor import select_top_news, process_news, process_github_repos
from mailer import send_email
import time

def main():
    print("Step 1: Fetching news and GitHub Agent data...")
    raw_news = fetch_news()
    github_data = fetch_github_agents()
    
    print("Step 2: Selecting Top 20 news and processing GitHub repos with AI...")
    top_news = select_top_news(raw_news, count=20)
    
    # 并行思想（逻辑上）：处理新闻和处理 GitHub 仓库
    print(f"Step 3: Generating summaries for {len(top_news)} news items...")
    processed_news = process_news(top_news)
    
    print("Step 4: Analyzing GitHub repositories (Types, Specs, Descriptions)...")
    processed_repos = process_github_repos(github_data)
    
    print("Step 5: Sending comprehensive daily email...")
    send_email(processed_news, processed_repos)
    
    print("Daily task completed successfully!")

if __name__ == "__main__":
    main()
