from fetcher import fetch_news
from processor import select_top_news, process_news
from mailer import send_email
import time

def main():
    print("Step 1: Fetching news from sources (Collecting 100 items for selection)...")
    raw_news = fetch_news()
    
    print("Step 2: Selecting Top 20 most popular/important news with Gemini AI...")
    top_news = select_top_news(raw_news, count=20)
    
    print(f"Step 3: Processing {len(top_news)} selected news with Gemini AI (Summarization & Translation)...")
    processed_news = process_news(top_news)
    
    print("Step 4: Sending daily email...")
    send_email(processed_news)
    
    print("Daily task completed!")

if __name__ == "__main__":
    main()
